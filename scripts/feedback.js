window.onUsersnapLoad = function(api) {
  api.init();
};
var script = document.createElement('script');
script.defer = 1;
script.src = 'https://widget.usersnap.com/global/load/eaffb19f-011a-4ff4-ad87-956a22981880?onload=onUsersnapLoad';
document.getElementsByTagName('head')[0].appendChild(script);

