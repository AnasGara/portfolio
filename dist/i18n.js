const language=document.documentElement.lang;
window.t=function(text){
  const pair=window.PortfolioTranslations?.[text];
  return pair&&language!=='en'?pair[language==='fr'?0:1]:text;
};
window.credentialCount=function(count){
  if(language==='fr')return `${count} badge${count===1?'':'s'}`;
  if(language==='de')return `${count} Nachweis${count===1?'':'e'}`;
  return `${count} credential${count===1?'':'s'}`;
};
const languageSelect=document.querySelector('#site-language');
languageSelect.value=language;
languageSelect.addEventListener('change',()=>{
  const routes={en:'/',fr:'/fr/',de:'/de/'};
  location.assign(routes[languageSelect.value]+location.hash);
});
document.querySelector('#theme-toggle').addEventListener('click',()=>{
  window.setPortfolioTheme(document.documentElement.dataset.theme==='light'?'dark':'light');
});
window.setPortfolioTheme(document.documentElement.dataset.theme);
