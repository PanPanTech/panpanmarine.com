'use strict';
(() => {
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.getElementById('navigation');
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      const open = toggle.getAttribute('aria-expanded') !== 'true';
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
      toggle.textContent = open ? 'Close' : 'Menu';
      nav.classList.toggle('open', open);
    });
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && nav.classList.contains('open')) { toggle.click(); toggle.focus(); }
    });
  }
  const filters = [...document.querySelectorAll('[data-filter]')];
  function filterEquipment(task) {
    const allowed = filters.map(b => b.dataset.filter);
    if (!allowed.includes(task)) throw new Error('Choose a valid equipment category.');
    let count = 0;
    document.querySelectorAll('#equipment-grid [data-task]').forEach(el => {
      el.hidden = task !== 'all' && el.dataset.task !== task;
      if (!el.hidden) count++;
    });
    filters.forEach(b => { b.classList.toggle('selected', b.dataset.filter === task); b.setAttribute('aria-pressed', String(b.dataset.filter === task)); });
    document.getElementById('filter-count').textContent = count + (count === 1 ? ' platform' : ' platforms');
    return {category: task, platforms: count};
  }
  filters.forEach(b => b.addEventListener('click', () => filterEquipment(b.dataset.filter)));
  const form = document.getElementById('proposal-form');
  let currentBrief = '';
  function prepareBrief(input) {
    if (!form) throw new Error('Open the project brief page first.');
    if (input) {
      const fields = ['name','email','company','country','task','model','description','depth','extent','conditions','timing'];
      Object.entries(input).forEach(([k,v]) => {
        if (!fields.includes(k) && k !== 'consent') throw new Error('Unknown brief field.');
        if (k === 'consent') {
          if (typeof v !== 'boolean') throw new Error('Consent must be true or false.');
        } else if (typeof v !== 'string') throw new Error('Brief fields must be text.');
      });
      const staged = {...Object.fromEntries(new FormData(form)), consent:form.elements.consent.checked, ...input};
      for (const k of ['name','email','company','country','description']) {
        const limit = form.elements[k].maxLength;
        if (!String(staged[k] || '').trim() || (limit > 0 && String(staged[k]).length > limit)) throw new Error('Complete the required fields within the allowed length.');
      }
      const emailCheck = document.createElement('input');
      emailCheck.type='email';emailCheck.required=true;emailCheck.value=staged.email;
      if (!emailCheck.checkValidity() || staged.consent !== true) throw new Error('Supply a valid email and acknowledge the privacy notice.');
      for (const k of ['task','model']) if (![...form.elements[k].options].some(o=>o.value===String(staged[k] || ''))) throw new Error('Choose a supported task and platform.');
      Object.entries(input).forEach(([k,v]) => { if (k === 'consent') form.elements[k].checked = v; else form.elements[k].value = v; });
    }
    if (!form.checkValidity()) { form.reportValidity(); throw new Error('Complete the required contact, task and privacy fields.'); }
    const data = Object.fromEntries(new FormData(form));
    const val = key => String(data[key] || 'Not specified').trim();
    const selected = key => form.elements[key].selectedOptions[0]?.textContent || val(key);
    currentBrief = ['UNDERWATER EQUIPMENT — PROJECT BRIEF','',`Name: ${val('name')}`,`Work email: ${val('email')}`,`Company: ${val('company')}`,`Country: ${val('country')}`,`Application: ${selected('task')}`,`Platform: ${selected('model')}`,'','Task and required result:',val('description'),'','SITE DETAILS',`Working depth: ${val('depth')}`,`Route / area: ${val('extent')}`,`Current / visibility: ${val('conditions')}`,`Procurement timing: ${val('timing')}`,'','Prepared locally. This document has not been sent to a sales team.'].join('\n');
    document.getElementById('brief-preview').textContent = currentBrief;
    document.getElementById('brief-result').hidden = false;
    document.getElementById('form-status').textContent = 'Your brief is ready to review. No inquiry has been sent.';
    document.getElementById('brief-result').scrollIntoView({behavior:'smooth',block:'start'});
    return {status:'prepared_not_sent',brief:currentBrief};
  }
  if (form) {
    const params = new URLSearchParams(location.search);
    ['task','model'].forEach(k => { const v=params.get(k); if ([...form.elements[k].options].some(o=>o.value===v)) form.elements[k].value=v; });
    form.addEventListener('submit', e => { e.preventDefault(); try { prepareBrief(); } catch (err) {document.getElementById('form-status').textContent=err.message;} });
    form.addEventListener('input', () => {
      if (currentBrief) { currentBrief=''; document.getElementById('brief-result').hidden=true; document.getElementById('form-status').textContent='Your details changed. Review the brief again to update it.'; }
    });
    document.getElementById('download-brief').addEventListener('click', () => {
      if (!currentBrief) return;
      const url=URL.createObjectURL(new Blob([currentBrief],{type:'text/plain;charset=utf-8'}));
      const a=document.createElement('a');a.href=url;a.download='underwater-equipment-project-brief.txt';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
    });
    document.getElementById('email-brief')?.addEventListener('click', () => {
      if (!currentBrief || !form.dataset.email) return;
      const mailto='mailto:'+encodeURIComponent(form.dataset.email)+'?subject='+encodeURIComponent('Underwater equipment project — '+form.elements.company.value)+'&body='+encodeURIComponent(currentBrief);
      location.href=mailto;
      document.getElementById('form-status').textContent='Email draft requested. Review and send it in your mail application.';
    });
  }
  // Progressive enhancement: use the same visible actions in WebMCP-capable browsers.
  if (document.modelContext?.registerTool) {
    const lifecycle = new AbortController();
    const register = tool => { try { Promise.resolve(document.modelContext.registerTool(tool,{signal:lifecycle.signal})).catch(()=>{}); } catch {} };
    if (filters.length) register({name:'filter_equipment',title:'Filter equipment',description:'Change the visible equipment category; does not submit an inquiry.',inputSchema:{type:'object',properties:{category:{type:'string',enum:['all','inspection','tunnel','cleaning','dredging']}},required:['category'],additionalProperties:false},annotations:{readOnlyHint:false},execute(input){if (!input || Object.keys(input).some(k=>k!=='category')) throw new Error('Supply only a category.');return filterEquipment(input.category);}});
    if (form) register({name:'prepare_project_brief',title:'Prepare project brief',description:'Populate and review a local equipment project brief. Does not send or store an inquiry.',inputSchema:{type:'object',properties:Object.fromEntries(['name','email','company','country','task','model','description','depth','extent','conditions','timing'].map(k=>[k,{type:'string'}]).concat([['consent',{type:'boolean'}]])),required:['name','email','company','country','description','consent'],additionalProperties:false},annotations:{readOnlyHint:false},execute:prepareBrief});
    window.addEventListener('pagehide',()=>lifecycle.abort(),{once:true});
  }
})();
