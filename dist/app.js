const icons = {aws:['amazonwebservices/amazonwebservices-original.svg','AWS'],terraform:['terraform/terraform-original.svg','Terraform'],ansible:['ansible/ansible-original.svg','Ansible'],docker:['docker/docker-original.svg','Docker'],kubernetes:['kubernetes/kubernetes-original.svg','Kubernetes'],linux:['linux/linux-original.svg','Linux'],githubactions:['githubactions/githubactions-original.svg','Actions'],jenkins:['jenkins/jenkins-original.svg','Jenkins'],gitlab:['gitlab/gitlab-original.svg','GitLab CI'],prometheus:['prometheus/prometheus-original.svg','Prometheus'],grafana:['grafana/grafana-original.svg','Grafana'],nginx:['nginx/nginx-original.svg','Nginx'],python:['python/python-original.svg','Python'],bash:['bash/bash-original.svg','Bash'],java:['java/java-original.svg','Java'],spring:['spring/spring-original.svg','Spring'],git:['git/git-original.svg','Git'],postgresql:['postgresql/postgresql-original.svg','Postgres']};
const svgStart = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 560 270" fill="none"><defs><pattern id="grid" width="18" height="18" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".65" fill="#748169" opacity=".2"/></pattern></defs><rect width="560" height="270" fill="url(#grid)"/>';
const label=(x,y,t,size=9,color='#66745d')=>`<text x="${x}" y="${y}" fill="${color}" font-family="Plex,monospace" font-size="${size}" text-anchor="middle">${t}</text>`;
const node=(x,y,w,h,t,accent=false)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="4" fill="${accent?'#f0a587':'#f3f4eb'}" stroke="${accent?'#bd6444':'#a5b096'}"/>${label(x+w/2,y+h/2+3,t,9,accent?'#8f462d':'#5f7154')}`;
const line=(d,accent=false)=>`<path d="${d}" stroke="${accent?'#bb6c4f':'#9aaa8c'}" stroke-dasharray="4 4"/>`;
const awsArt=svgStart+`<rect x="80" y="60" width="400" height="161" rx="7" stroke="#b8c2ab" stroke-dasharray="5 4"/>${label(280,81,'AWS / MULTI-AZ VPC',8)}${node(233,96,94,30,'HTTPS / ALB',true)}${line('M280 126V144M172 144H388M172 144V157M388 144V157')}${node(122,157,100,30,'EC2 / AZ-A')}${node(338,157,100,30,'EC2 / AZ-B')}${line('M172 187V205H388V187')}${node(233,189,94,29,'RDS / Multi-AZ')}${label(172,242,'PRIVATE SUBNET',7)}${label(388,242,'PRIVATE SUBNET',7)}</svg>`;
const serverlessArt=svgStart+`${node(45,116,91,39,'API GATEWAY')}${line('M136 136H173')}${node(173,116,90,39,'LAMBDA',true)}${line('M263 136H300')}${node(300,116,85,39,'SQS')}${line('M385 136H423')}${node(423,116,93,39,'DELIVERY')}${line('M218 116V78H342V116')}${node(245,60,113,33,'DYNAMODB')}${line('M342 155V203H468V155')}${label(402,198,'RETRY / DLQ',8)}${label(280,237,'INGEST → ROUTE → DELIVER',8)}</svg>`;
const tracesArt=svgStart+`${node(45,117,90,37,'GATEWAY')}${line('M135 135H188')}${node(188,78,97,34,'CLIENT')}${node(188,158,97,34,'PORTAL')}${line('M162 135V94H188M162 135V175H188')}${line('M285 95H327V175H285M327 135H375')}${node(375,117,127,37,'ZIPKIN / TRACES',true)}<path d="M390 174h18v8h37v8h33" stroke="#ba6c50" stroke-width="3"/>${node(200,218,174,27,'POSTGRESQL / DOCKER')}${line('M235 192V218')}${label(438,211,'REQUEST VISIBILITY',7)}</svg>`;
const deliveryArt=svgStart+`<rect x="66" y="72" width="430" height="129" rx="6" fill="#282e27"/>${label(153,96,'Jenkinsfile',8,'#9ba890')}<circle cx="83" cy="87" r="3" fill="#de835c"/><circle cx="95" cy="87" r="3" fill="#acb791"/><circle cx="107" cy="87" r="3" fill="#798b72"/><path d="M66 107H496" stroke="#515a48"/>${node(87,132,79,35,'BUILD')}${line('M166 150H188')}${node(188,132,79,35,'TEST')}${line('M267 150H290')}${node(290,132,88,35,'PACKAGE',true)}${line('M378 150H400')}${node(400,132,76,35,'RUN')}${label(280,231,'MAVEN → DOCKER → COMPOSE',8)}</svg>`;
const projects=[
{id:'aws-infrastructure',category:'CLOUD ARCHITECTURE / INFRASTRUCTURE AS CODE',filter:'cloud',title:'Infrastructure, without the guesswork.',description:'A repeatable AWS foundation: two availability zones, private compute, and a database designed for resilience.',tags:['AWS','Terraform','GitHub Actions'],art:awsArt,url:'https://github.com/AnasGara/AWS---Scalable-infrastructure---Terraform',details:['Modular Terraform for networking, compute, and Multi-AZ PostgreSQL, with encrypted remote state.','An HTTPS application load balancer fronts private EC2 Auto Scaling instances across two availability zones.','GitHub Actions validates changes and uses OIDC for deployment; operations runbooks cover recovery and teardown.'],boundary:'Reference infrastructure with documented local verification. Live AWS acceptance, quotas, failover, and DNS/TLS checks remain a separate deployment step.'},
{id:'webhook-platform',category:'SERVERLESS / EVENT-DRIVEN SYSTEMS',filter:'cloud',title:'Every event has somewhere to go.',description:'A tenant-isolated webhook router with authenticated ingestion, asynchronous delivery, retries, and an audit trail.',tags:['AWS SAM','Python','Lambda','SQS'],art:serverlessArt,url:'https://github.com/AnasGara/DBaas-Project/tree/main/webhook-router',details:['API Gateway and Lambda handle authenticated ingestion and dynamic event routing.','DynamoDB holds tenant routing and audit records; a transactional outbox coordinates delivery.','SQS retries and dead-letter handling make failed delivery visible and recoverable, supported by CloudWatch alarms.'],boundary:'An engineering project in the DBaas-Project repository. Implementation and local verification are documented; live AWS acceptance is a separate step.'},
{id:'distributed-tracing',category:'MICROSERVICES / OBSERVABILITY',filter:'observability',title:'Follow the request. Find the answer.',description:'A Spring microservices demonstration that connects discovery, routing, and distributed traces in one understandable system.',tags:['Spring Cloud','Docker','Zipkin','PostgreSQL'],art:tracesArt,url:'https://github.com/AnasGara/Microservices-Portals-Clients-with-SpringBoot-and-Zipkin',details:['Spring Cloud Config centralizes configuration, Eureka provides service discovery, and a gateway routes requests.','Client and portal services communicate with OpenFeign and use separate PostgreSQL databases.','Micrometer and Zipkin expose request paths, with Docker Compose providing local database and tracing infrastructure.'],boundary:'A demonstration and local development project. Repository documentation explains service startup order and infrastructure setup.'},
{id:'delivery-lab',category:'CI/CD / CONTAINER DELIVERY',filter:'delivery',title:'From source code to a running service.',description:'A focused delivery lab that joins Java builds, container packaging, and application startup in a Jenkins pipeline.',tags:['Jenkins','Java','Maven','Docker'],art:deliveryArt,url:'https://github.com/AnasGara/BasicApp-SpringBoot-Docker-Jenkins',details:['A declarative Jenkins pipeline connects application build steps into a repeatable workflow.','Maven builds the Spring Boot application, and a Dockerfile packages the service.','Docker Compose provides application startup configuration, keeping the application and delivery workflow together.'],boundary:'A learning project for CI/CD and containerization. It illustrates the delivery workflow rather than claiming a managed production service.'}
];
const grid=document.querySelector('#project-grid');
grid.innerHTML=projects.map((p,i)=>`<article class="project-card" data-category="${p.filter}"><button class="project-visual" data-project="${p.id}" aria-label="Read about ${p.title}"><span class="visual-label">SYSTEM STUDY / 0${i+1}</span>${p.art}<span class="project-open" aria-hidden="true">↗</span></button><div class="project-card-top"><span class="project-category">${p.category}</span><span class="project-number">0${i+1} / 04</span></div><h3><button data-project="${p.id}">${p.title}</button></h3><p>${p.description}</p><div class="tags">${p.tags.map(t=>`<span>${t}</span>`).join('')}</div></article>`).join('');
document.querySelectorAll('[data-filter]').forEach(button=>button.addEventListener('click',()=>{document.querySelectorAll('[data-filter]').forEach(b=>{const selected=b===button;b.classList.toggle('active',selected);b.setAttribute('aria-pressed',String(selected));});document.querySelectorAll('.project-card').forEach(card=>{card.hidden=button.dataset.filter!=='all'&&card.dataset.category!==button.dataset.filter;});}));
const dialog=document.querySelector('#project-dialog');let dialogOpener;
document.querySelectorAll('[data-project]').forEach(button=>button.addEventListener('click',()=>{const p=projects.find(p=>p.id===button.dataset.project);dialogOpener=button;document.querySelector('#dialog-content').innerHTML=`<div class="dialog-visual">${p.art}</div><div class="dialog-category">${p.category}</div><h2 id="dialog-title">${p.title}</h2><p class="dialog-description">${p.description}</p><ul class="dialog-details">${p.details.map(d=>`<li>${d}</li>`).join('')}</ul><p class="dialog-boundary">${p.boundary}</p><div class="dialog-actions"><div class="tags">${p.tags.map(t=>`<span>${t}</span>`).join('')}</div><a class="button button-dark" href="${p.url}" target="_blank" rel="noopener noreferrer">Explore the source <span>↗</span></a></div>`;dialog.showModal();dialog.scrollTop=0;}));
document.querySelector('.dialog-close').addEventListener('click',()=>dialog.close());dialog.addEventListener('click',e=>{if(e.target===dialog){const b=dialog.getBoundingClientRect();if(e.clientX<b.left||e.clientX>b.right||e.clientY<b.top||e.clientY>b.bottom)dialog.close();}});dialog.addEventListener('close',()=>dialogOpener?.focus());
const toolGroups=[['Cloud & infrastructure',['aws','terraform','ansible'],'EC2, S3, RDS, Lambda, Route 53, ALB, Auto Scaling, WAF. Azure & GCP fundamentals.'],['Containers & systems',['docker','kubernetes','linux'],'Containerization, orchestration, Linux administration, and VMware virtualization.'],['Build & delivery',['githubactions','jenkins','gitlab'],'Automated builds and tests, branch-based deployments, and repeatable releases.'],['Observe & protect',['prometheus','grafana','nginx'],'Metrics, dashboards, DNS, TLS, ingress, SonarQube, Zipkin, and ELK/OpenSearch.'],['Scripting & backend',['python','bash','java','spring'],'Automation scripts, Spring Boot services, APIs, SQL, and application debugging.'],['Data & collaboration',['git','postgresql'],'Version control, relational databases, technical documentation, and Agile/Scrum.']];
document.querySelector('#toolbox-grid').innerHTML=toolGroups.map(([name,tools,desc],i)=>`<div class="tool-group"><div class="tool-heading">${name}<span>0${i+1}</span></div><div class="tool-icons">${tools.map(t=>`<div class="tool"><img src="assets/icons/${t}.svg" alt="" width="29" height="27" loading="lazy"><span>${icons[t][1]}</span></div>`).join('')}</div><p>${desc}</p></div>`).join('');
const menuToggle=document.querySelector('.menu-toggle');const nav=document.querySelector('.header nav');menuToggle.addEventListener('click',()=>{const open=menuToggle.getAttribute('aria-expanded')!=='true';menuToggle.setAttribute('aria-expanded',String(open));menuToggle.setAttribute('aria-label',open?'Close navigation':'Open navigation');nav.classList.toggle('is-open',open);});nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>{menuToggle.setAttribute('aria-expanded','false');menuToggle.setAttribute('aria-label','Open navigation');nav.classList.remove('is-open');}));document.addEventListener('keydown',e=>{if(e.key==='Escape'&&nav.classList.contains('is-open')){menuToggle.click();menuToggle.focus();}});
const stages=['Code / Start with the application and its needs.','Automate / Build, test, and release repeatably.','Operate / Scale, observe, and keep improving.'];let stage=-1;const selectStage=n=>{stage=n;document.querySelectorAll('[data-stage]').forEach(el=>el.classList.toggle('is-selected',Number(el.dataset.stage)===n));document.querySelector('#stage-caption').textContent=stages[n];document.querySelector('.stage-indicator').textContent=`0${n+1} / 03`;};document.querySelectorAll('[data-stage]').forEach(el=>{el.addEventListener('click',()=>selectStage(Number(el.dataset.stage)));el.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();selectStage(Number(el.dataset.stage));}});});document.querySelector('#next-stage').addEventListener('click',()=>selectStage((stage+1)%3));
let copyTimer;document.querySelector('.copy-email').addEventListener('click',async()=>{const status=document.querySelector('#copy-status');clearTimeout(copyTimer);try{await navigator.clipboard.writeText('anasgara7@gmail.com');status.textContent='Copied!';}catch{status.textContent='Select email to copy';const range=document.createRange();range.selectNodeContents(document.querySelector('.email-wrap>a'));const selection=window.getSelection();selection.removeAllRanges();selection.addRange(range);}copyTimer=setTimeout(()=>status.textContent='',2800);});

// Credential cards remain useful as ordinary verification links without JavaScript.
const credentialCards=[...document.querySelectorAll('.credential-card')];
document.querySelectorAll('[data-credential-filter]').forEach(button=>button.addEventListener('click',()=>{
  const provider=button.dataset.credentialFilter;
  document.querySelectorAll('[data-credential-filter]').forEach(control=>{
    const selected=control===button;
    control.classList.toggle('active',selected);
    control.setAttribute('aria-pressed',String(selected));
  });
  let visible=0;
  credentialCards.forEach(card=>{
    card.hidden=provider!=='all'&&card.dataset.provider!==provider;
    if(!card.hidden){visible++;card.classList.add('is-revealed');}
  });
  document.querySelector('#credential-count').textContent=`${visible} credential${visible===1?'':'s'}`;
}));

const reducedMotion=window.matchMedia('(prefers-reduced-motion: reduce)');
const art=document.querySelector('.system-art');
art.addEventListener('pointermove',event=>{
  if(reducedMotion.matches||event.pointerType!=='mouse')return;
  const bounds=art.getBoundingClientRect();
  art.style.setProperty('--tilt-x',`${-((event.clientY-bounds.top)/bounds.height-.5)*5}deg`);
  art.style.setProperty('--tilt-y',`${((event.clientX-bounds.left)/bounds.width-.5)*5}deg`);
});
art.addEventListener('pointerleave',()=>{art.style.removeProperty('--tilt-x');art.style.removeProperty('--tilt-y');});

let scrollFrame=0;
function updateReadingProgress(){
  const max=document.documentElement.scrollHeight-window.innerHeight;
  document.documentElement.style.setProperty('--reading-progress',String(max>0?window.scrollY/max:0));
  scrollFrame=0;
}
window.addEventListener('scroll',()=>{if(!scrollFrame)scrollFrame=requestAnimationFrame(updateReadingProgress);},{passive:true});
window.addEventListener('resize',updateReadingProgress);
updateReadingProgress();

if('IntersectionObserver' in window){
  const navObserver=new IntersectionObserver(entries=>{
    entries.forEach(entry=>{
      const link=document.querySelector(`.header nav a[href="#${entry.target.id}"]`);
      if(link)link.classList.toggle('is-current',entry.isIntersecting);
    });
  },{rootMargin:'-20% 0px -55% 0px'});
  document.querySelectorAll('main section[id]').forEach(section=>navObserver.observe(section));

  if(!reducedMotion.matches){
    const revealObserver=new IntersectionObserver(entries=>{
      entries.forEach(entry=>{
        if(!entry.isIntersecting)return;
        entry.target.classList.add('is-revealed');
        revealObserver.unobserve(entry.target);
      });
    },{threshold:.08,rootMargin:'0px 0px -30px 0px'});
    document.querySelectorAll('.section-heading,.project-card,.about-intro,.about-copy,.experience-row,.tool-group,.credential-card,.education>div,.contact-inner').forEach((el,index)=>{
      el.classList.add('reveal-ready');
      el.style.setProperty('--reveal-delay',`${(index%3)*65}ms`);
      revealObserver.observe(el);
    });
    const metricObserver=new IntersectionObserver(entries=>{
      entries.forEach(entry=>{
        if(!entry.isIntersecting)return;
        const metric=entry.target;
        const textNode=metric.querySelector('strong').firstChild;
        const target=Number(textNode.nodeValue.trim());
        const start=performance.now();
        metric.classList.add('is-counting');
        const frame=now=>{
          const progress=Math.min((now-start)/1100,1);
          textNode.nodeValue=String(Math.round(target*(1-Math.pow(1-progress,3))));
          if(progress<1)requestAnimationFrame(frame);
          else metric.classList.remove('is-counting');
        };
        requestAnimationFrame(frame);
        metricObserver.unobserve(metric);
      });
    },{threshold:.5});
    document.querySelectorAll('.metric').forEach(metric=>metricObserver.observe(metric));
    reducedMotion.addEventListener('change',event=>{
      if(event.matches){document.querySelectorAll('.reveal-ready').forEach(el=>el.classList.add('is-revealed'));revealObserver.disconnect();}
    });
  }
}

