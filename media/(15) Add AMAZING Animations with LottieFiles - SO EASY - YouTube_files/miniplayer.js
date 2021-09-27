(function(g){var window=this;'use strict';var A6=function(a){g.U.call(this,{G:"div",L:"ytp-miniplayer-ui"});this.ke=!1;this.player=a;this.T(a,"minimized",this.qg);this.T(a,"onStateChange",this.tF)},B6=function(a){g.cN.call(this,a);
this.i=new A6(this.player);this.i.hide();g.RM(this.player,this.i.element,4);a.Ce()&&(this.load(),g.O(a.getRootNode(),"ytp-player-minimized",!0))};
g.w(A6,g.U);g.k=A6.prototype;
g.k.yD=function(){this.tooltip=new g.AQ(this.player,this);g.J(this,this.tooltip);g.RM(this.player,this.tooltip.element,4);this.tooltip.scale=.6;this.lc=new g.WN(this.player);g.J(this,this.lc);this.yg=new g.U({G:"div",L:"ytp-miniplayer-scrim"});g.J(this,this.yg);this.yg.Ea(this.element);this.T(this.yg.element,"click",this.yz);var a=new g.U({G:"button",Ha:["ytp-miniplayer-close-button","ytp-button"],X:{"aria-label":"Close"},U:[g.bL()]});g.J(this,a);a.Ea(this.yg.element);this.T(a.element,"click",this.oi);
a=new g.U1(this.player,this);g.J(this,a);a.Ea(this.yg.element);this.bp=new g.U({G:"div",L:"ytp-miniplayer-controls"});g.J(this,this.bp);this.bp.Ea(this.yg.element);this.T(this.bp.element,"click",this.yz);var b=new g.U({G:"div",L:"ytp-miniplayer-button-container"});g.J(this,b);b.Ea(this.bp.element);a=new g.U({G:"div",L:"ytp-miniplayer-play-button-container"});g.J(this,a);a.Ea(this.bp.element);var c=new g.U({G:"div",L:"ytp-miniplayer-button-container"});g.J(this,c);c.Ea(this.bp.element);this.YL=new g.tP(this.player,
this,!1);g.J(this,this.YL);this.YL.Ea(b.element);b=new g.rP(this.player,this);g.J(this,b);b.Ea(a.element);this.nextButton=new g.tP(this.player,this,!0);g.J(this,this.nextButton);this.nextButton.Ea(c.element);this.Bg=new g.mQ(this.player,this);g.J(this,this.Bg);this.Bg.Ea(this.yg.element);this.Kc=new g.zP(this.player,this);g.J(this,this.Kc);g.RM(this.player,this.Kc.element,4);this.kz=new g.U({G:"div",L:"ytp-miniplayer-buttons"});g.J(this,this.kz);g.RM(this.player,this.kz.element,4);a=new g.U({G:"button",
Ha:["ytp-miniplayer-close-button","ytp-button"],X:{"aria-label":"Close"},U:[g.bL()]});g.J(this,a);a.Ea(this.kz.element);this.T(a.element,"click",this.oi);a=new g.U({G:"button",Ha:["ytp-miniplayer-replay-button","ytp-button"],X:{"aria-label":"Close"},U:[g.gL()]});g.J(this,a);a.Ea(this.kz.element);this.T(a.element,"click",this.vU);this.T(this.player,"presentingplayerstatechange",this.Ic);this.T(this.player,"appresize",this.wb);this.T(this.player,"fullscreentoggled",this.wb);this.wb()};
g.k.show=function(){this.Bd=new g.yq(this.Sp,null,this);this.Bd.start();this.ke||(this.yD(),this.ke=!0);0!==this.player.getPlayerState()&&g.U.prototype.show.call(this);this.Kc.show();this.player.unloadModule("annotations_module")};
g.k.hide=function(){this.Bd&&(this.Bd.dispose(),this.Bd=void 0);g.U.prototype.hide.call(this);this.player.Ce()||(this.ke&&this.Kc.hide(),this.player.loadModule("annotations_module"))};
g.k.ya=function(){this.Bd&&(this.Bd.dispose(),this.Bd=void 0);g.U.prototype.ya.call(this)};
g.k.oi=function(){this.player.stopVideo();this.player.Na("onCloseMiniplayer")};
g.k.vU=function(){this.player.playVideo()};
g.k.yz=function(a){if(a.target===this.yg.element||a.target===this.bp.element)this.player.W().N("kevlar_miniplayer_play_pause_on_scrim")?g.eK(this.player.vb())?this.player.pauseVideo():this.player.playVideo():this.player.Na("onExpandMiniplayer")};
g.k.qg=function(){g.O(this.player.getRootNode(),"ytp-player-minimized",this.player.Ce())};
g.k.jd=function(){this.Kc.Nb();this.Bg.Nb()};
g.k.Sp=function(){this.jd();this.Bd&&this.Bd.start()};
g.k.Ic=function(a){g.T(a.state,32)&&this.tooltip.hide()};
g.k.wb=function(){g.MP(this.Kc,0,this.player.eb().getPlayerSize().width,!1);g.AP(this.Kc)};
g.k.tF=function(a){this.player.Ce()&&(0===a?this.hide():this.show())};
g.k.dc=function(){return this.tooltip};
g.k.Ke=function(){return!1};
g.k.hf=function(){return!1};
g.k.ci=function(){return!1};
g.k.hA=function(){};
g.k.Pm=function(){};
g.k.xr=function(){};
g.k.jn=function(){return null};
g.k.aj=function(){return new g.Cl(0,0,0,0)};
g.k.handleGlobalKeyDown=function(){return!1};
g.k.handleGlobalKeyUp=function(){return!1};
g.k.Zp=function(a,b,c,d,e){var f=0,h=d=0,l=g.Yl(a);if(b){c=g.Jq(b,"ytp-prev-button")||g.Jq(b,"ytp-next-button");var m=g.Jq(b,"ytp-play-button"),n=g.Jq(b,"ytp-miniplayer-expand-watch-page-button");c?f=h=12:m?(b=g.Wl(b,this.element),h=b.x,f=b.y-12):n&&(h=g.Jq(b,"ytp-miniplayer-button-top-left"),f=g.Wl(b,this.element),b=g.Yl(b),h?(h=8,f=f.y+40):(h=f.x-l.width+b.width,f=f.y-20))}else h=c-l.width/2,d=25+(e||0);b=this.player.eb().getPlayerSize().width;e=f+(e||0);l=g.Zf(h,0,b-l.width);e?(a.style.top=e+"px",
a.style.bottom=""):(a.style.top="",a.style.bottom=d+"px");a.style.left=l+"px"};
g.k.showControls=function(){};
g.k.Ok=function(){};
g.k.jk=function(){return!1};g.w(B6,g.cN);B6.prototype.create=function(){};
B6.prototype.Di=function(){return!1};
B6.prototype.load=function(){this.player.hideControls();this.i.show()};
B6.prototype.unload=function(){this.player.showControls();this.i.hide()};g.bN("miniplayer",B6);})(_yt_player);
