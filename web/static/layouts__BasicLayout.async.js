(window.webpackJsonp=window.webpackJsonp||[]).push([[1],{"3a4m":function(e,a,t){e.exports=t("usdK").default},Kkfi:function(e,a,t){e.exports={menu:"antd-pro-components-select-lang-index-menu",dropDown:"antd-pro-components-select-lang-index-dropDown"}},QyDn:function(e,a,t){e.exports={container:"antd-pro-components-header-dropdown-index-container"}},bx7e:function(e,a,t){"use strict";t.r(a);var n=t("gWZ8"),r=t.n(n),o=t("p0pE"),c=t.n(o),l=(t("Pwec"),t("CtXQ")),s=(t("5Dmo"),t("3S7+")),u=t("2Taf"),i=t.n(u),m=t("vZ4D"),d=t.n(m),p=t("l4Ni"),g=t.n(p),f=t("ujKo"),h=t.n(f),v=t("MhPg"),y=t.n(v),b=t("q1tI"),E=t.n(b),k=t("Y2fQ"),x=(t("lUTK"),t("BvKs")),N=t("TSYQ"),C=t.n(N),M=(t("qVdP"),t("jsC+")),O=t("Y/ft"),j=t.n(O),w=t("QyDn"),z=t.n(w),T=function(e){var a=e.overlayClassName,t=j()(e,["overlayClassName"]);return E.a.createElement(M.a,Object.assign({overlayClassName:C()(z.a.container,a)},t))},R=t("Kkfi"),D=t.n(R),F=function(e){var a=e.className,t=Object(k.getLocale)(),n={"zh-CN":"简体中文","zh-TW":"繁体中文","en-US":"English","pt-BR":"Português"},r={"zh-CN":"🇨🇳","zh-TW":"🇭🇰","en-US":"🇬🇧","pt-BR":"🇧🇷"},o=E.a.createElement(x.a,{className:D.a.menu,selectedKeys:[t],onClick:function(e){var a=e.key;return Object(k.setLocale)(a,!1)}},["zh-CN","zh-TW","en-US","pt-BR"].map(function(e){return E.a.createElement(x.a.Item,{key:e},E.a.createElement("span",{role:"img","aria-label":n[e]},r[e])," ",n[e])}));return E.a.createElement(T,{overlay:o,placement:"bottomRight"},E.a.createElement("span",{className:C()(D.a.dropDown,a)},E.a.createElement(l.a,{type:"global",title:Object(k.formatMessage)({id:"navBar.lang"})})))},K=t("h3zL"),P=t.n(K),S=(t("T2oS"),t("W9HT")),B=(t("Telt"),t("Tckk")),L=t("MuoO"),I=t("3a4m"),U=t.n(I),_=function(e){function a(){var e;return i()(this,a),(e=g()(this,h()(a).apply(this,arguments))).onMenuClick=function(a){var t=a.key;if("logout"!==t)U.a.push("/account/".concat(t));else{var n=e.props.dispatch;n&&n({type:"login/logout"})}},e}return y()(a,e),d()(a,[{key:"render",value:function(){var e=this.props,a=e.currentUser,t=void 0===a?{}:a;if(!e.menu)return E.a.createElement("span",{className:"".concat(P.a.action," ").concat(P.a.account)},E.a.createElement(B.a,{size:"small",className:P.a.avatar,src:t.avatar,alt:"avatar"}),E.a.createElement("span",{className:P.a.name},t.name));var n=E.a.createElement(x.a,{className:P.a.menu,selectedKeys:[],onClick:this.onMenuClick},E.a.createElement(x.a.Item,{key:"center"},E.a.createElement(l.a,{type:"user"}),E.a.createElement(k.FormattedMessage,{id:"menu.account.center",defaultMessage:"account center"})),E.a.createElement(x.a.Item,{key:"settings"},E.a.createElement(l.a,{type:"setting"}),E.a.createElement(k.FormattedMessage,{id:"menu.account.settings",defaultMessage:"account settings"})),E.a.createElement(x.a.Divider,null),E.a.createElement(x.a.Item,{key:"logout"},E.a.createElement(l.a,{type:"logout"}),E.a.createElement(k.FormattedMessage,{id:"menu.account.logout",defaultMessage:"logout"})));return t&&t.name?E.a.createElement(T,{overlay:n},E.a.createElement("span",{className:"".concat(P.a.action," ").concat(P.a.account)},E.a.createElement(B.a,{size:"small",className:P.a.avatar,src:t.avatar,alt:"avatar"}),E.a.createElement("span",{className:P.a.name},t.name))):E.a.createElement(S.a,{size:"small",style:{marginLeft:8,marginRight:8}})}}]),a}(E.a.Component),Q=Object(L.connect)(function(e){return{currentUser:e.user.currentUser}})(_),W=function(e){function a(){return i()(this,a),g()(this,h()(a).apply(this,arguments))}return y()(a,e),d()(a,[{key:"render",value:function(){var e=this.props,a=e.theme,t=e.layout,n=P.a.right;return"dark"===a&&"topmenu"===t&&(n="".concat(P.a.right,"  ").concat(P.a.dark)),E.a.createElement("div",{className:n},E.a.createElement(s.a,{title:Object(k.formatMessage)({id:"component.globalHeader.help"})},E.a.createElement("a",{target:"_blank",href:"https://github.com/mrzhangboss/FlinkSQLPlatform",rel:"noopener noreferrer",className:P.a.action},E.a.createElement(l.a,{type:"github"}))),E.a.createElement(Q,null),E.a.createElement(F,null))}}]),a}(b.Component),Y=Object(L.connect)(function(e){var a=e.settings;return{theme:a.navTheme,layout:a.layout}})(W),H=t("mxmt"),q=t.n(H),J=t("eTk0"),Z=t("Hx5s"),V=t("wY1l"),X=t.n(V),A=function e(a){return a.map(function(a){var t=c()({},a,{children:a.children?e(a.children):[]});return J.a.check(a.authority,t,null)})},G=function(e,a){return E.a.createElement(E.a.Fragment,null)};a.default=Object(L.connect)(function(e){var a=e.global,t=e.settings;return{collapsed:a.collapsed,settings:t}})(function(e){var a=e.dispatch,t=e.children,n=e.settings;Object(b.useState)(function(){a&&(a({type:"user/fetchCurrent"}),a({type:"settings/getSetting"}))});return E.a.createElement(Z.a,Object.assign({logo:q.a,onCollapse:function(e){return a&&a({type:"global/changeLayoutCollapsed",payload:e})},menuItemRender:function(e,a){return E.a.createElement(X.a,{to:e.path},a)},breadcrumbRender:function(){var e=arguments.length>0&&void 0!==arguments[0]?arguments[0]:[];return[{path:"/",breadcrumbName:Object(k.formatMessage)({id:"menu.home",defaultMessage:"Home"})}].concat(r()(e))},footerRender:G,menuDataRender:A,formatMessage:k.formatMessage,rightContentRender:function(e){return E.a.createElement(Y,Object.assign({},e))}},e,n),t)})},h3zL:function(e,a,t){e.exports={logo:"antd-pro-components-global-header-index-logo",menu:"antd-pro-components-global-header-index-menu",trigger:"antd-pro-components-global-header-index-trigger",right:"antd-pro-components-global-header-index-right",action:"antd-pro-components-global-header-index-action",search:"antd-pro-components-global-header-index-search",account:"antd-pro-components-global-header-index-account",avatar:"antd-pro-components-global-header-index-avatar",dark:"antd-pro-components-global-header-index-dark",name:"antd-pro-components-global-header-index-name"}},mOP9:function(e,a,t){"use strict";Object.defineProperty(a,"__esModule",{value:!0}),a.default=void 0;var n=t("55Ip").Link;a.default=n},mxmt:function(e,a,t){e.exports=t.p+"static/logo.7203683c.svg"},usdK:function(e,a,t){"use strict";Object.defineProperty(a,"__esModule",{value:!0}),a.push=o,a.replace=c,a.go=l,a.goBack=s,a.goForward=u,a.default=void 0;var n,r=(n=t("RFCh"))&&n.__esModule?n:{default:n};function o(){r.default.push.apply(r.default,arguments)}function c(){r.default.replace.apply(r.default,arguments)}function l(){r.default.go.apply(r.default,arguments)}function s(){r.default.goBack.apply(r.default,arguments)}function u(){r.default.goForward.apply(r.default,arguments)}var i={push:o,replace:c,go:l,goBack:s,goForward:u};a.default=i},wY1l:function(e,a,t){e.exports=t("mOP9").default}}]);