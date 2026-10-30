// Apply the saved palette before stylesheets paint, including on translated routes.
window.setPortfolioTheme=function(theme){
  const light=theme==='light';
  document.documentElement.dataset.theme=light?'light':'dark';
  document.querySelector('meta[name="theme-color"]')?.setAttribute('content',light?'#f5f3ed':'#090f16');
  try{localStorage.setItem('portfolio-theme',light?'light':'dark');}catch{}
  const button=document.querySelector('#theme-toggle');
  if(button){
    const translate=window.t||((s)=>s);
    button.setAttribute('aria-pressed',String(light));
    button.setAttribute('aria-label',translate(light?'Switch to dark mode':'Switch to light mode'));
    button.title=translate(light?'Switch to dark mode':'Switch to light mode');
    button.querySelector('.theme-label').textContent=translate(light?'Dark':'Light');
    button.querySelector('.theme-icon').textContent=light?'☾':'☼';
  }
};
let initialTheme='dark';try{if(localStorage.getItem('portfolio-theme')==='light')initialTheme='light';}catch{}
window.setPortfolioTheme(initialTheme);
