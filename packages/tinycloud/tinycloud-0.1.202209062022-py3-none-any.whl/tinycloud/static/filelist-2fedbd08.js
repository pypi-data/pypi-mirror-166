/**
 * @license
 * Copyright 2019 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const t$1=window,e$2=t$1.ShadowRoot&&(void 0===t$1.ShadyCSS||t$1.ShadyCSS.nativeShadow)&&"adoptedStyleSheets"in Document.prototype&&"replace"in CSSStyleSheet.prototype,s$3=Symbol(),n$3=new WeakMap;class o$4{constructor(t,e,n){if(this._$cssResult$=!0,n!==s$3)throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");this.cssText=t,this.t=e;}get styleSheet(){let t=this.o;const s=this.t;if(e$2&&void 0===t){const e=void 0!==s&&1===s.length;e&&(t=n$3.get(s)),void 0===t&&((this.o=t=new CSSStyleSheet).replaceSync(this.cssText),e&&n$3.set(s,t));}return t}toString(){return this.cssText}}const r$2=t=>new o$4("string"==typeof t?t:t+"",void 0,s$3),i$1=(t,...e)=>{const n=1===t.length?t[0]:e.reduce(((e,s,n)=>e+(t=>{if(!0===t._$cssResult$)return t.cssText;if("number"==typeof t)return t;throw Error("Value passed to 'css' function must be a 'css' function result: "+t+". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.")})(s)+t[n+1]),t[0]);return new o$4(n,t,s$3)},S$1=(s,n)=>{e$2?s.adoptedStyleSheets=n.map((t=>t instanceof CSSStyleSheet?t:t.styleSheet)):n.forEach((e=>{const n=document.createElement("style"),o=t$1.litNonce;void 0!==o&&n.setAttribute("nonce",o),n.textContent=e.cssText,s.appendChild(n);}));},c$1=e$2?t=>t:t=>t instanceof CSSStyleSheet?(t=>{let e="";for(const s of t.cssRules)e+=s.cssText;return r$2(e)})(t):t;

/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */var s$2;const e$1=window,r$1=e$1.trustedTypes,h$1=r$1?r$1.emptyScript:"",o$3=e$1.reactiveElementPolyfillSupport,n$2={toAttribute(t,i){switch(i){case Boolean:t=t?h$1:null;break;case Object:case Array:t=null==t?t:JSON.stringify(t);}return t},fromAttribute(t,i){let s=t;switch(i){case Boolean:s=null!==t;break;case Number:s=null===t?null:Number(t);break;case Object:case Array:try{s=JSON.parse(t);}catch(t){s=null;}}return s}},a$1=(t,i)=>i!==t&&(i==i||t==t),l$2={attribute:!0,type:String,converter:n$2,reflect:!1,hasChanged:a$1};class d$1 extends HTMLElement{constructor(){super(),this._$Ei=new Map,this.isUpdatePending=!1,this.hasUpdated=!1,this._$El=null,this.u();}static addInitializer(t){var i;null!==(i=this.h)&&void 0!==i||(this.h=[]),this.h.push(t);}static get observedAttributes(){this.finalize();const t=[];return this.elementProperties.forEach(((i,s)=>{const e=this._$Ep(s,i);void 0!==e&&(this._$Ev.set(e,s),t.push(e));})),t}static createProperty(t,i=l$2){if(i.state&&(i.attribute=!1),this.finalize(),this.elementProperties.set(t,i),!i.noAccessor&&!this.prototype.hasOwnProperty(t)){const s="symbol"==typeof t?Symbol():"__"+t,e=this.getPropertyDescriptor(t,s,i);void 0!==e&&Object.defineProperty(this.prototype,t,e);}}static getPropertyDescriptor(t,i,s){return {get(){return this[i]},set(e){const r=this[t];this[i]=e,this.requestUpdate(t,r,s);},configurable:!0,enumerable:!0}}static getPropertyOptions(t){return this.elementProperties.get(t)||l$2}static finalize(){if(this.hasOwnProperty("finalized"))return !1;this.finalized=!0;const t=Object.getPrototypeOf(this);if(t.finalize(),this.elementProperties=new Map(t.elementProperties),this._$Ev=new Map,this.hasOwnProperty("properties")){const t=this.properties,i=[...Object.getOwnPropertyNames(t),...Object.getOwnPropertySymbols(t)];for(const s of i)this.createProperty(s,t[s]);}return this.elementStyles=this.finalizeStyles(this.styles),!0}static finalizeStyles(i){const s=[];if(Array.isArray(i)){const e=new Set(i.flat(1/0).reverse());for(const i of e)s.unshift(c$1(i));}else void 0!==i&&s.push(c$1(i));return s}static _$Ep(t,i){const s=i.attribute;return !1===s?void 0:"string"==typeof s?s:"string"==typeof t?t.toLowerCase():void 0}u(){var t;this._$E_=new Promise((t=>this.enableUpdating=t)),this._$AL=new Map,this._$Eg(),this.requestUpdate(),null===(t=this.constructor.h)||void 0===t||t.forEach((t=>t(this)));}addController(t){var i,s;(null!==(i=this._$ES)&&void 0!==i?i:this._$ES=[]).push(t),void 0!==this.renderRoot&&this.isConnected&&(null===(s=t.hostConnected)||void 0===s||s.call(t));}removeController(t){var i;null===(i=this._$ES)||void 0===i||i.splice(this._$ES.indexOf(t)>>>0,1);}_$Eg(){this.constructor.elementProperties.forEach(((t,i)=>{this.hasOwnProperty(i)&&(this._$Ei.set(i,this[i]),delete this[i]);}));}createRenderRoot(){var t;const s=null!==(t=this.shadowRoot)&&void 0!==t?t:this.attachShadow(this.constructor.shadowRootOptions);return S$1(s,this.constructor.elementStyles),s}connectedCallback(){var t;void 0===this.renderRoot&&(this.renderRoot=this.createRenderRoot()),this.enableUpdating(!0),null===(t=this._$ES)||void 0===t||t.forEach((t=>{var i;return null===(i=t.hostConnected)||void 0===i?void 0:i.call(t)}));}enableUpdating(t){}disconnectedCallback(){var t;null===(t=this._$ES)||void 0===t||t.forEach((t=>{var i;return null===(i=t.hostDisconnected)||void 0===i?void 0:i.call(t)}));}attributeChangedCallback(t,i,s){this._$AK(t,s);}_$EO(t,i,s=l$2){var e;const r=this.constructor._$Ep(t,s);if(void 0!==r&&!0===s.reflect){const h=(void 0!==(null===(e=s.converter)||void 0===e?void 0:e.toAttribute)?s.converter:n$2).toAttribute(i,s.type);this._$El=t,null==h?this.removeAttribute(r):this.setAttribute(r,h),this._$El=null;}}_$AK(t,i){var s;const e=this.constructor,r=e._$Ev.get(t);if(void 0!==r&&this._$El!==r){const t=e.getPropertyOptions(r),h="function"==typeof t.converter?{fromAttribute:t.converter}:void 0!==(null===(s=t.converter)||void 0===s?void 0:s.fromAttribute)?t.converter:n$2;this._$El=r,this[r]=h.fromAttribute(i,t.type),this._$El=null;}}requestUpdate(t,i,s){let e=!0;void 0!==t&&(((s=s||this.constructor.getPropertyOptions(t)).hasChanged||a$1)(this[t],i)?(this._$AL.has(t)||this._$AL.set(t,i),!0===s.reflect&&this._$El!==t&&(void 0===this._$EC&&(this._$EC=new Map),this._$EC.set(t,s))):e=!1),!this.isUpdatePending&&e&&(this._$E_=this._$Ej());}async _$Ej(){this.isUpdatePending=!0;try{await this._$E_;}catch(t){Promise.reject(t);}const t=this.scheduleUpdate();return null!=t&&await t,!this.isUpdatePending}scheduleUpdate(){return this.performUpdate()}performUpdate(){var t;if(!this.isUpdatePending)return;this.hasUpdated,this._$Ei&&(this._$Ei.forEach(((t,i)=>this[i]=t)),this._$Ei=void 0);let i=!1;const s=this._$AL;try{i=this.shouldUpdate(s),i?(this.willUpdate(s),null===(t=this._$ES)||void 0===t||t.forEach((t=>{var i;return null===(i=t.hostUpdate)||void 0===i?void 0:i.call(t)})),this.update(s)):this._$Ek();}catch(t){throw i=!1,this._$Ek(),t}i&&this._$AE(s);}willUpdate(t){}_$AE(t){var i;null===(i=this._$ES)||void 0===i||i.forEach((t=>{var i;return null===(i=t.hostUpdated)||void 0===i?void 0:i.call(t)})),this.hasUpdated||(this.hasUpdated=!0,this.firstUpdated(t)),this.updated(t);}_$Ek(){this._$AL=new Map,this.isUpdatePending=!1;}get updateComplete(){return this.getUpdateComplete()}getUpdateComplete(){return this._$E_}shouldUpdate(t){return !0}update(t){void 0!==this._$EC&&(this._$EC.forEach(((t,i)=>this._$EO(i,this[i],t))),this._$EC=void 0),this._$Ek();}updated(t){}firstUpdated(t){}}d$1.finalized=!0,d$1.elementProperties=new Map,d$1.elementStyles=[],d$1.shadowRootOptions={mode:"open"},null==o$3||o$3({ReactiveElement:d$1}),(null!==(s$2=e$1.reactiveElementVersions)&&void 0!==s$2?s$2:e$1.reactiveElementVersions=[]).push("1.4.1");

/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
var t;const i=window,s$1=i.trustedTypes,e=s$1?s$1.createPolicy("lit-html",{createHTML:t=>t}):void 0,o$2=`lit$${(Math.random()+"").slice(9)}$`,n$1="?"+o$2,l$1=`<${n$1}>`,h=document,r=(t="")=>h.createComment(t),d=t=>null===t||"object"!=typeof t&&"function"!=typeof t,u=Array.isArray,c=t=>u(t)||"function"==typeof(null==t?void 0:t[Symbol.iterator]),v=/<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,a=/-->/g,f=/>/g,_=RegExp(">|[ \t\n\f\r](?:([^\\s\"'>=/]+)([ \t\n\f\r]*=[ \t\n\f\r]*(?:[^ \t\n\f\r\"'`<>=]|(\"|')|))|$)","g"),m=/'/g,p=/"/g,$=/^(?:script|style|textarea|title)$/i,g=t=>(i,...s)=>({_$litType$:t,strings:i,values:s}),y=g(1),x=Symbol.for("lit-noChange"),b=Symbol.for("lit-nothing"),T=new WeakMap,A=(t,i,s)=>{var e,o;const n=null!==(e=null==s?void 0:s.renderBefore)&&void 0!==e?e:i;let l=n._$litPart$;if(void 0===l){const t=null!==(o=null==s?void 0:s.renderBefore)&&void 0!==o?o:null;n._$litPart$=l=new S(i.insertBefore(r(),t),t,void 0,null!=s?s:{});}return l._$AI(t),l},E=h.createTreeWalker(h,129,null,!1),C=(t,i)=>{const s=t.length-1,n=[];let h,r=2===i?"<svg>":"",d=v;for(let i=0;i<s;i++){const s=t[i];let e,u,c=-1,g=0;for(;g<s.length&&(d.lastIndex=g,u=d.exec(s),null!==u);)g=d.lastIndex,d===v?"!--"===u[1]?d=a:void 0!==u[1]?d=f:void 0!==u[2]?($.test(u[2])&&(h=RegExp("</"+u[2],"g")),d=_):void 0!==u[3]&&(d=_):d===_?">"===u[0]?(d=null!=h?h:v,c=-1):void 0===u[1]?c=-2:(c=d.lastIndex-u[2].length,e=u[1],d=void 0===u[3]?_:'"'===u[3]?p:m):d===p||d===m?d=_:d===a||d===f?d=v:(d=_,h=void 0);const y=d===_&&t[i+1].startsWith("/>")?" ":"";r+=d===v?s+l$1:c>=0?(n.push(e),s.slice(0,c)+"$lit$"+s.slice(c)+o$2+y):s+o$2+(-2===c?(n.push(void 0),i):y);}const u=r+(t[s]||"<?>")+(2===i?"</svg>":"");if(!Array.isArray(t)||!t.hasOwnProperty("raw"))throw Error("invalid template strings array");return [void 0!==e?e.createHTML(u):u,n]};class P{constructor({strings:t,_$litType$:i},e){let l;this.parts=[];let h=0,d=0;const u=t.length-1,c=this.parts,[v,a]=C(t,i);if(this.el=P.createElement(v,e),E.currentNode=this.el.content,2===i){const t=this.el.content,i=t.firstChild;i.remove(),t.append(...i.childNodes);}for(;null!==(l=E.nextNode())&&c.length<u;){if(1===l.nodeType){if(l.hasAttributes()){const t=[];for(const i of l.getAttributeNames())if(i.endsWith("$lit$")||i.startsWith(o$2)){const s=a[d++];if(t.push(i),void 0!==s){const t=l.getAttribute(s.toLowerCase()+"$lit$").split(o$2),i=/([.?@])?(.*)/.exec(s);c.push({type:1,index:h,name:i[2],strings:t,ctor:"."===i[1]?R:"?"===i[1]?H:"@"===i[1]?I:M});}else c.push({type:6,index:h});}for(const i of t)l.removeAttribute(i);}if($.test(l.tagName)){const t=l.textContent.split(o$2),i=t.length-1;if(i>0){l.textContent=s$1?s$1.emptyScript:"";for(let s=0;s<i;s++)l.append(t[s],r()),E.nextNode(),c.push({type:2,index:++h});l.append(t[i],r());}}}else if(8===l.nodeType)if(l.data===n$1)c.push({type:2,index:h});else {let t=-1;for(;-1!==(t=l.data.indexOf(o$2,t+1));)c.push({type:7,index:h}),t+=o$2.length-1;}h++;}}static createElement(t,i){const s=h.createElement("template");return s.innerHTML=t,s}}function V(t,i,s=t,e){var o,n,l,h;if(i===x)return i;let r=void 0!==e?null===(o=s._$Cl)||void 0===o?void 0:o[e]:s._$Cu;const u=d(i)?void 0:i._$litDirective$;return (null==r?void 0:r.constructor)!==u&&(null===(n=null==r?void 0:r._$AO)||void 0===n||n.call(r,!1),void 0===u?r=void 0:(r=new u(t),r._$AT(t,s,e)),void 0!==e?(null!==(l=(h=s)._$Cl)&&void 0!==l?l:h._$Cl=[])[e]=r:s._$Cu=r),void 0!==r&&(i=V(t,r._$AS(t,i.values),r,e)),i}class N{constructor(t,i){this.v=[],this._$AN=void 0,this._$AD=t,this._$AM=i;}get parentNode(){return this._$AM.parentNode}get _$AU(){return this._$AM._$AU}p(t){var i;const{el:{content:s},parts:e}=this._$AD,o=(null!==(i=null==t?void 0:t.creationScope)&&void 0!==i?i:h).importNode(s,!0);E.currentNode=o;let n=E.nextNode(),l=0,r=0,d=e[0];for(;void 0!==d;){if(l===d.index){let i;2===d.type?i=new S(n,n.nextSibling,this,t):1===d.type?i=new d.ctor(n,d.name,d.strings,this,t):6===d.type&&(i=new L(n,this,t)),this.v.push(i),d=e[++r];}l!==(null==d?void 0:d.index)&&(n=E.nextNode(),l++);}return o}m(t){let i=0;for(const s of this.v)void 0!==s&&(void 0!==s.strings?(s._$AI(t,s,i),i+=s.strings.length-2):s._$AI(t[i])),i++;}}class S{constructor(t,i,s,e){var o;this.type=2,this._$AH=b,this._$AN=void 0,this._$AA=t,this._$AB=i,this._$AM=s,this.options=e,this._$C_=null===(o=null==e?void 0:e.isConnected)||void 0===o||o;}get _$AU(){var t,i;return null!==(i=null===(t=this._$AM)||void 0===t?void 0:t._$AU)&&void 0!==i?i:this._$C_}get parentNode(){let t=this._$AA.parentNode;const i=this._$AM;return void 0!==i&&11===t.nodeType&&(t=i.parentNode),t}get startNode(){return this._$AA}get endNode(){return this._$AB}_$AI(t,i=this){t=V(this,t,i),d(t)?t===b||null==t||""===t?(this._$AH!==b&&this._$AR(),this._$AH=b):t!==this._$AH&&t!==x&&this.$(t):void 0!==t._$litType$?this.T(t):void 0!==t.nodeType?this.k(t):c(t)?this.O(t):this.$(t);}S(t,i=this._$AB){return this._$AA.parentNode.insertBefore(t,i)}k(t){this._$AH!==t&&(this._$AR(),this._$AH=this.S(t));}$(t){this._$AH!==b&&d(this._$AH)?this._$AA.nextSibling.data=t:this.k(h.createTextNode(t)),this._$AH=t;}T(t){var i;const{values:s,_$litType$:e}=t,o="number"==typeof e?this._$AC(t):(void 0===e.el&&(e.el=P.createElement(e.h,this.options)),e);if((null===(i=this._$AH)||void 0===i?void 0:i._$AD)===o)this._$AH.m(s);else {const t=new N(o,this),i=t.p(this.options);t.m(s),this.k(i),this._$AH=t;}}_$AC(t){let i=T.get(t.strings);return void 0===i&&T.set(t.strings,i=new P(t)),i}O(t){u(this._$AH)||(this._$AH=[],this._$AR());const i=this._$AH;let s,e=0;for(const o of t)e===i.length?i.push(s=new S(this.S(r()),this.S(r()),this,this.options)):s=i[e],s._$AI(o),e++;e<i.length&&(this._$AR(s&&s._$AB.nextSibling,e),i.length=e);}_$AR(t=this._$AA.nextSibling,i){var s;for(null===(s=this._$AP)||void 0===s||s.call(this,!1,!0,i);t&&t!==this._$AB;){const i=t.nextSibling;t.remove(),t=i;}}setConnected(t){var i;void 0===this._$AM&&(this._$C_=t,null===(i=this._$AP)||void 0===i||i.call(this,t));}}class M{constructor(t,i,s,e,o){this.type=1,this._$AH=b,this._$AN=void 0,this.element=t,this.name=i,this._$AM=e,this.options=o,s.length>2||""!==s[0]||""!==s[1]?(this._$AH=Array(s.length-1).fill(new String),this.strings=s):this._$AH=b;}get tagName(){return this.element.tagName}get _$AU(){return this._$AM._$AU}_$AI(t,i=this,s,e){const o=this.strings;let n=!1;if(void 0===o)t=V(this,t,i,0),n=!d(t)||t!==this._$AH&&t!==x,n&&(this._$AH=t);else {const e=t;let l,h;for(t=o[0],l=0;l<o.length-1;l++)h=V(this,e[s+l],i,l),h===x&&(h=this._$AH[l]),n||(n=!d(h)||h!==this._$AH[l]),h===b?t=b:t!==b&&(t+=(null!=h?h:"")+o[l+1]),this._$AH[l]=h;}n&&!e&&this.P(t);}P(t){t===b?this.element.removeAttribute(this.name):this.element.setAttribute(this.name,null!=t?t:"");}}class R extends M{constructor(){super(...arguments),this.type=3;}P(t){this.element[this.name]=t===b?void 0:t;}}const k=s$1?s$1.emptyScript:"";class H extends M{constructor(){super(...arguments),this.type=4;}P(t){t&&t!==b?this.element.setAttribute(this.name,k):this.element.removeAttribute(this.name);}}class I extends M{constructor(t,i,s,e,o){super(t,i,s,e,o),this.type=5;}_$AI(t,i=this){var s;if((t=null!==(s=V(this,t,i,0))&&void 0!==s?s:b)===x)return;const e=this._$AH,o=t===b&&e!==b||t.capture!==e.capture||t.once!==e.once||t.passive!==e.passive,n=t!==b&&(e===b||o);o&&this.element.removeEventListener(this.name,this,e),n&&this.element.addEventListener(this.name,this,t),this._$AH=t;}handleEvent(t){var i,s;"function"==typeof this._$AH?this._$AH.call(null!==(s=null===(i=this.options)||void 0===i?void 0:i.host)&&void 0!==s?s:this.element,t):this._$AH.handleEvent(t);}}class L{constructor(t,i,s){this.element=t,this.type=6,this._$AN=void 0,this._$AM=i,this.options=s;}get _$AU(){return this._$AM._$AU}_$AI(t){V(this,t);}}const Z=i.litHtmlPolyfillSupport;null==Z||Z(P,S),(null!==(t=i.litHtmlVersions)&&void 0!==t?t:i.litHtmlVersions=[]).push("2.3.1");

/**
 * @license
 * Copyright 2017 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */var l,o$1;class s extends d$1{constructor(){super(...arguments),this.renderOptions={host:this},this._$Dt=void 0;}createRenderRoot(){var t,e;const i=super.createRenderRoot();return null!==(t=(e=this.renderOptions).renderBefore)&&void 0!==t||(e.renderBefore=i.firstChild),i}update(t){const i=this.render();this.hasUpdated||(this.renderOptions.isConnected=this.isConnected),super.update(t),this._$Dt=A(i,this.renderRoot,this.renderOptions);}connectedCallback(){var t;super.connectedCallback(),null===(t=this._$Dt)||void 0===t||t.setConnected(!0);}disconnectedCallback(){var t;super.disconnectedCallback(),null===(t=this._$Dt)||void 0===t||t.setConnected(!1);}render(){return x}}s.finalized=!0,s._$litElement$=!0,null===(l=globalThis.litElementHydrateSupport)||void 0===l||l.call(globalThis,{LitElement:s});const n=globalThis.litElementPolyfillSupport;null==n||n({LitElement:s});(null!==(o$1=globalThis.litElementVersions)&&void 0!==o$1?o$1:globalThis.litElementVersions=[]).push("3.2.0");

/**
 * @license
 * Copyright 2021 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const o=(o,r,n)=>{for(const n of r)if(n[0]===o)return (0, n[1])();return null==n?void 0:n()};

/**
 * @license
 * Copyright 2021 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const isStrTagged = (val) => typeof val !== 'string' && 'strTag' in val;
/**
 * Render the result of a `str` tagged template to a string. Note we don't need
 * to do this for Lit templates, since Lit itself handles rendering.
 */
const joinStringsAndValues = (strings, values, valueOrder) => {
    let concat = strings[0];
    for (let i = 1; i < strings.length; i++) {
        concat += values[valueOrder ? valueOrder[i - 1] : i - 1];
        concat += strings[i];
    }
    return concat;
};

/**
 * @license
 * Copyright 2021 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
/**
 * Default identity msg implementation. Simply returns the input template with
 * no awareness of translations. If the template is str-tagged, returns it in
 * string form.
 */
const defaultMsg = ((template) => isStrTagged(template)
    ? joinStringsAndValues(template.strings, template.values)
    : template);

/**
 * @license
 * Copyright 2021 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
/**
 * Name of the event dispatched to `window` whenever a locale change starts,
 * finishes successfully, or fails. Only relevant to runtime mode.
 *
 * The `detail` of this event is an object with a `status` string that can be:
 * "loading", "ready", or "error", along with the relevant locale code, and
 * error message if applicable.
 *
 * You can listen for this event to know when your application should be
 * re-rendered following a locale change. See also the Localized mixin, which
 * automatically re-renders LitElement classes using this event.
 */
const LOCALE_STATUS_EVENT = 'lit-localize-status';

/**
 * @license
 * Copyright 2021 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
class LocalizeController {
    constructor(host) {
        this.__litLocalizeEventHandler = (event) => {
            if (event.detail.status === 'ready') {
                this.host.requestUpdate();
            }
        };
        this.host = host;
    }
    hostConnected() {
        window.addEventListener(LOCALE_STATUS_EVENT, this.__litLocalizeEventHandler);
    }
    hostDisconnected() {
        window.removeEventListener(LOCALE_STATUS_EVENT, this.__litLocalizeEventHandler);
    }
}
/**
 * Re-render the given LitElement whenever a new active locale has loaded.
 *
 * See also {@link localized} for the same functionality as a decorator.
 *
 * When using lit-localize in transform mode, calls to this function are
 * replaced with undefined.
 *
 * Usage:
 *
 *   import {LitElement, html} from 'lit';
 *   import {msg, updateWhenLocaleChanges} from '@lit/localize';
 *
 *   class MyElement extends LitElement {
 *     constructor() {
 *       super();
 *       updateWhenLocaleChanges(this);
 *     }
 *
 *     render() {
 *       return html`<b>${msg('Hello World')}</b>`;
 *     }
 *   }
 */
const _updateWhenLocaleChanges = (host) => host.addController(new LocalizeController(host));
const updateWhenLocaleChanges = _updateWhenLocaleChanges;

/**
 * @license
 * Copyright 2020 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
class Deferred {
    constructor() {
        this.settled = false;
        this.promise = new Promise((resolve, reject) => {
            this._resolve = resolve;
            this._reject = reject;
        });
    }
    resolve(value) {
        this.settled = true;
        this._resolve(value);
    }
    reject(error) {
        this.settled = true;
        this._reject(error);
    }
}

/**
 * @license
 * Copyright 2014 Travis Webb
 * SPDX-License-Identifier: MIT
 */
// This module is derived from the file:
// https://github.com/tjwebb/fnv-plus/blob/1e2ce68a07cb7dd4c3c85364f3d8d96c95919474/index.js#L309
//
// Changes:
// - Only the _hash64_1a_fast function is included.
// - Removed loop unrolling.
// - Converted to TypeScript ES module.
// - var -> let/const
//
// TODO(aomarks) Upstream improvements to https://github.com/tjwebb/fnv-plus/.
const hl = [];
for (let i = 0; i < 256; i++) {
    hl[i] = ((i >> 4) & 15).toString(16) + (i & 15).toString(16);
}
/**
 * Perform a FNV-1A 64-bit hash of the given string (as UTF-16 code units), and
 * return a hexadecimal digest (left zero padded to 16 characters).
 *
 * @see {@link http://tools.ietf.org/html/draft-eastlake-fnv-06}
 */
function fnv1a64(str) {
    let t0 = 0, v0 = 0x2325, t1 = 0, v1 = 0x8422, t2 = 0, v2 = 0x9ce4, t3 = 0, v3 = 0xcbf2;
    for (let i = 0; i < str.length; i++) {
        v0 ^= str.charCodeAt(i);
        t0 = v0 * 435;
        t1 = v1 * 435;
        t2 = v2 * 435;
        t3 = v3 * 435;
        t2 += v0 << 8;
        t3 += v1 << 8;
        t1 += t0 >>> 16;
        v0 = t0 & 65535;
        t2 += t1 >>> 16;
        v1 = t1 & 65535;
        v3 = (t3 + (t2 >>> 16)) & 65535;
        v2 = t2 & 65535;
    }
    return (hl[v3 >> 8] +
        hl[v3 & 255] +
        hl[v2 >> 8] +
        hl[v2 & 255] +
        hl[v1 >> 8] +
        hl[v1 & 255] +
        hl[v0 >> 8] +
        hl[v0 & 255]);
}

/**
 * @license
 * Copyright 2020 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
/**
 * Delimiter used between each template string component before hashing. Used to
 * prevent e.g. "foobar" and "foo${baz}bar" from sharing a hash.
 *
 * This is the "record separator" ASCII character.
 */
const HASH_DELIMITER = '\x1e';
/**
 * Id prefix on html-tagged templates to distinguish e.g. `<b>x</b>` from
 * html`<b>x</b>`.
 */
const HTML_PREFIX = 'h';
/**
 * Id prefix on plain string templates to distinguish e.g. `<b>x</b>` from
 * html`<b>x</b>`.
 */
const STRING_PREFIX = 's';
/**
 * Generate a unique ID for a lit-localize message.
 *
 * Example:
 *   Template: html`Hello <b>${who}</b>!`
 *     Params: ["Hello <b>", "</b>!"], true
 *     Output: h82ccc38d4d46eaa9
 *
 * The ID is constructed as:
 *
 *   [0]    Kind of template: [h]tml or [s]tring.
 *   [1,16] 64-bit FNV-1a hash hex digest of the template strings, as UTF-16
 *          code points, delineated by an ASCII "record separator" character.
 *
 * We choose FNV-1a because:
 *
 *   1. It's pretty fast (e.g. much faster than SHA-1).
 *   2. It's pretty small (0.25 KiB minified + brotli).
 *   3. We don't require cryptographic security, and 64 bits should give
 *      sufficient collision resistance for any one application. Worst
 *      case, we will always detect collisions during analysis.
 *   4. We can't use Web Crypto API (e.g. SHA-1), because it's asynchronous.
 *   5. It's a well known non-cryptographic hash with implementations in many
 *      languages.
 *   6. There was an existing JavaScript implementation that doesn't require
 *      BigInt, for IE11 compatibility.
 */
function generateMsgId(strings, isHtmlTagged) {
    return ((isHtmlTagged ? HTML_PREFIX : STRING_PREFIX) +
        fnv1a64(typeof strings === 'string' ? strings : strings.join(HASH_DELIMITER)));
}

/**
 * @license
 * Copyright 2021 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
const expressionOrders = new WeakMap();
const hashCache = new Map();
function runtimeMsg(templates, template, options) {
    var _a;
    if (templates) {
        const id = (_a = options === null || options === void 0 ? void 0 : options.id) !== null && _a !== void 0 ? _a : generateId(template);
        const localized = templates[id];
        if (localized) {
            if (typeof localized === 'string') {
                // E.g. "Hello World!"
                return localized;
            }
            else if ('strTag' in localized) {
                // E.g. str`Hello ${name}!`
                //
                // Localized templates have ${number} in place of real template
                // expressions. They can't have real template values, because the
                // variable scope would be wrong. The number tells us the index of the
                // source value to substitute in its place, because expressions can be
                // moved to a different position during translation.
                return joinStringsAndValues(localized.strings, 
                // Cast `template` because its type wasn't automatically narrowed (but
                // we know it must be the same type as `localized`).
                template.values, localized.values);
            }
            else {
                // E.g. html`Hello <b>${name}</b>!`
                //
                // We have to keep our own mapping of expression ordering because we do
                // an in-place update of `values`, and otherwise we'd lose ordering for
                // subsequent renders.
                let order = expressionOrders.get(localized);
                if (order === undefined) {
                    order = localized.values;
                    expressionOrders.set(localized, order);
                }
                return {
                    ...localized,
                    values: order.map((i) => template.values[i]),
                };
            }
        }
    }
    return defaultMsg(template);
}
function generateId(template) {
    const strings = typeof template === 'string' ? template : template.strings;
    let id = hashCache.get(strings);
    if (id === undefined) {
        id = generateMsgId(strings, typeof template !== 'string' && !('strTag' in template));
        hashCache.set(strings, id);
    }
    return id;
}

/**
 * @license
 * Copyright 2021 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
/**
 * Dispatch a "lit-localize-status" event to `window` with the given detail.
 */
function dispatchStatusEvent(detail) {
    window.dispatchEvent(new CustomEvent(LOCALE_STATUS_EVENT, { detail }));
}
let activeLocale = '';
let loadingLocale;
let sourceLocale;
let validLocales;
let loadLocale;
let templates;
let loading = new Deferred();
// The loading promise must be initially resolved, because that's what we should
// return if the user immediately calls setLocale(sourceLocale).
loading.resolve();
let requestId = 0;
/**
 * Set configuration parameters for lit-localize when in runtime mode. Returns
 * an object with functions:
 *
 * - `getLocale`: Return the active locale code.
 * - `setLocale`: Set the active locale code.
 *
 * Throws if called more than once.
 */
const configureLocalization = (config) => {
    _installMsgImplementation(((template, options) => runtimeMsg(templates, template, options)));
    activeLocale = sourceLocale = config.sourceLocale;
    validLocales = new Set(config.targetLocales);
    validLocales.add(config.sourceLocale);
    loadLocale = config.loadLocale;
    return { getLocale, setLocale };
};
/**
 * Return the active locale code.
 */
const getLocale = () => {
    return activeLocale;
};
/**
 * Set the active locale code, and begin loading templates for that locale using
 * the `loadLocale` function that was passed to `configureLocalization`. Returns
 * a promise that resolves when the next locale is ready to be rendered.
 *
 * Note that if a second call to `setLocale` is made while the first requested
 * locale is still loading, then the second call takes precedence, and the
 * promise returned from the first call will resolve when second locale is
 * ready. If you need to know whether a particular locale was loaded, check
 * `getLocale` after the promise resolves.
 *
 * Throws if the given locale is not contained by the configured `sourceLocale`
 * or `targetLocales`.
 */
const setLocale = (newLocale) => {
    if (newLocale === (loadingLocale !== null && loadingLocale !== void 0 ? loadingLocale : activeLocale)) {
        return loading.promise;
    }
    if (!validLocales || !loadLocale) {
        throw new Error('Internal error');
    }
    if (!validLocales.has(newLocale)) {
        throw new Error('Invalid locale code');
    }
    requestId++;
    const thisRequestId = requestId;
    loadingLocale = newLocale;
    if (loading.settled) {
        loading = new Deferred();
    }
    dispatchStatusEvent({ status: 'loading', loadingLocale: newLocale });
    const localePromise = newLocale === sourceLocale
        ? // We could switch to the source locale synchronously, but we prefer to
            // queue it on a microtask so that switching locales is consistently
            // asynchronous.
            Promise.resolve({ templates: undefined })
        : loadLocale(newLocale);
    localePromise.then((mod) => {
        if (requestId === thisRequestId) {
            activeLocale = newLocale;
            loadingLocale = undefined;
            templates = mod.templates;
            dispatchStatusEvent({ status: 'ready', readyLocale: newLocale });
            loading.resolve();
        }
        // Else another locale was requested in the meantime. Don't resolve or
        // reject, because the newer load call is going to use the same promise.
        // Note the user can call getLocale() after the promise resolves if they
        // need to check if the locale is still the one they expected to load.
    }, (err) => {
        if (requestId === thisRequestId) {
            dispatchStatusEvent({
                status: 'error',
                errorLocale: newLocale,
                errorMessage: err.toString(),
            });
            loading.reject(err);
        }
    });
    return loading.promise;
};

/**
 * @license
 * Copyright 2020 Google LLC
 * SPDX-License-Identifier: BSD-3-Clause
 */
/**
 * Make a string or lit-html template localizable.
 *
 * @param template A string, a lit-html template, or a function that returns
 * either a string or lit-html template.
 * @param options Optional configuration object with the following properties:
 *   - id: Optional project-wide unique identifier for this template. If
 *     omitted, an id will be automatically generated from the template strings.
 *   - desc: Optional description
 */
let msg = defaultMsg;
let installed = false;
/**
 * Internal only. Do not use this function.
 *
 * Installs an implementation of the msg function to replace the default
 * identity function. Throws if called more than once.
 *
 * @internal
 */
function _installMsgImplementation(impl) {
    if (installed) {
        throw new Error('lit-localize can only be configured once');
    }
    msg = impl;
    installed = true;
}

function cleanPath(pathstr) {
  return "/" + pathstr.split("/").filter(x => x != "").join("/");
}
function setCookie(key, value, exp) {
  document.cookie = key + "=" + value; //+ "; max-age=" +exp;
}

class tc_contextmenu extends s {
  static properties = {
    menu: {}
  };
  static styles = i$1`div{width:200px;border:1px solid #999;background-color:var(--tc-ctxmenu-color,gray);position:absolute;top:10px;left:10px;display:none;z-index:9999999}ul{list-style:none}a:hover{background:var(--tc-link-color,#fff)}`;
  show = ev => {
    ev.preventDefault();
    var e = ev || window.event;
    var context = this.shadowRoot.getElementById("context");
    context.style.display = "block";
    var x = e.pageX;
    var y = e.pageY;
    context.style.left = x + "px";
    context.style.top = y + "px";
    return false;
  };
  close = () => {
    this.shadowRoot.getElementById("context").style.display = "none";
  };

  constructor() {
    super();
  }

  render() {
    var res = [];
    var item;

    for (item in this.menu) {
      res.push(y`<li><a @click="${this.menu[item]}">${item}</a></li>`);
    }

    return y`<div id="context"><ul>${res}</ul></div>`;
  }

}
customElements.define("tc-contextmenu", tc_contextmenu);

class tc_shares extends s {
  static properties = {
    shares: {}
  };
  static styles = i$1`a{color:var(--tc-link-color,#00f);text-decoration:none}`;

  constructor() {
    super();
    this.token = localStorage["token"];
  }

  loadData() {
    fetch("/api/shares").then(resp => {
      resp.json().then(res => {
        this.shares = res;
      });
    });
  }

  render() {
    if (!this.shares) {
      return;
    }

    var h = [];

    for (var i in this.shares) {
      var path = this.shares[i].path;

      if (path == "") {
        path = "/";
      }

      h.push(y`<a href="/shares/${i}">${location.origin}/shares/${i}</a> Path: ${path} | User:${this.shares[i].username}<button>del</button><br>`);
    }

    return y`${h}`;
  }

}
class tc_newshare extends s {
  static properties = {
    path: {}
  };
  static styles = i$1`#newshare{width:30%;height:25%;overflow:auto;margin:auto;position:fixed;top:0;left:0;bottom:0;right:0;z-index:99999;background-color:inherit}`;

  constructor() {
    super();
  }

  createShare() {
    fetch("/api/shares/new", {
      method: "POST",
      header: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        path: this.path,
        mode: this.shadowRoot.getElementById("write").checked && "rw" || "r"
      })
    }).then(this.remove());
  }

  render() {
    return y`<div id="newshare">${msg("Create share")} ${this.path}<br><input id="write" type="checkbox">${msg("Write access")}<br><button @click="${this.remove}">${msg("Cancel")}</button><button @click="${this.createShare}">${msg("Create")}</button></div>`;
  }

}
customElements.define("tc-shares", tc_shares);
customElements.define("tc-newshare", tc_newshare);

class tc_filelist extends s {
  static properties = {
    files: {},
    url: {},
    urlRoot: {},
    menu: {},
    file_upload: {},
    showHidden: {},
    apiBase: {},
    readOnly: {},
    token: {}
  };
  static styles = i$1`a{color:var(--tc-link-color,#00f)}.mountpoint{color:green}.broken{color:red}`;
  loadData = () => {
    if (this.file_upload) {
      this.file_upload.style.display = "none";
    }

    return fetch(this.apiBase + this.url + "?json_mode=1", {
      method: "PROPFIND"
    }).then(res => {
      if (res.ok) {
        if (this.file_upload) {
          this.file_upload.style.display = "block";
        }

        res.json().then(res => {
          var files = res.files.sort((a, b) => {
            return a["name"] > b["name"];
          });
          var mountPoint = [];
          files.forEach((item, index) => {
            if (item.type === "mountpoint") {
              mountPoint.push(item);
              files.splice(index, 1);
              return;
            }
          });

          if (mountPoint.length) {
            var i;

            for (i in mountPoint) {
              files.unshift(mountPoint[i]);
            }
          }

          this.files = files;
        });
      } else {
        location.href = "#" + this.url.split("/").slice(0, -2).join("/");

        switch (res.status) {
          case 404:
            alert(msg("No such file or directory"));
            break;

          case 403:
            alert(msg("Permission denied"));
            break;
        }
      }
    });
  };
  delete_file = filename => {
    if (!confirm(msg("Delete file?"))) {
      return 0;
    }

    fetch(this.apiBase + this.url + "/" + filename + "?json_mode=1", {
      method: "DELETE"
    }).then(res => {
      if (res.ok) {
        this.loadData();
      }
    });
  };
  mkdir = dirname => {
    fetch(this.apiBase + this.url + "/" + dirname + "?json_mode=1", {
      method: "MKCOL"
    }).then(res => {
      if (res.ok) {
        this.loadData();
      }
    });
  };
  contextmenu = e => {
    if (e.target.getAttribute("tc-filename")) {
      e.preventDefault();
      var filename = e.target.getAttribute("tc-filename");
      this.menu.menu = {
        [msg("Open file")]: () => {
          window.open(this.apiBase + this.url + "/" + filename);
        },
        [msg("Download file")]: () => {
          var m = document.createEvent("MouseEvents");
          m.initEvent("click", true, true);
          e.originalTarget.dispatchEvent(m);
        }
      };

      if (!this.readOnly) {
        this.menu.menu[msg("Create share")] = () => {
          var newshare = new tc_newshare();
          newshare.path = cleanPath(this.url + "/" + filename);
          this.shadowRoot.appendChild(newshare);
        };

        this.menu.menu[msg("Delete file")] = () => {
          this.delete_file(filename);
        };
      }
    } else {
      this.menu.menu = {
        [msg("Show hidden files")]: () => {
          this.showHidden = !this.showHidden;
          localStorage.setItem("showHidden", this.showHidden);
        }
      };

      if (!this.readOnly) {
        this.menu.menu[msg("New folder")] = () => {
          name = prompt("文件夹名");
          this.mkdir(name);
        };

        if (this.file_upload) {
          this.menu.menu[msg("Upload file")] = () => {
            this.file_upload.input_form.click();
          };
        }
      }
    }

    this.menu.show(e);
  };

  constructor() {
    super();
    updateWhenLocaleChanges(this);

    if (localStorage.getItem("showHidden") != null) {
      this.showHidden = localStorage.getItem("showHidden");
    } else {
      this.showHidden = false;
    }

    this.menu = new tc_contextmenu();
    this.url = "/";
    this.apiBase = "/dav/";
    this.readOnly = false;
    this.token = localStorage["token"];
  }

  hasFile(filename) {
    var i;

    for (i in this.files) {
      if (this.files[i].name == filename) {
        return Number(i);
      }
    }
  }

  scrollToFile(file) {
    var fileElement = this.shadowRoot.getElementById("file-" + file);
    fileElement.scrollIntoView({
      behavior: "smooth"
    });
    fileElement.style.background = "gray";
    setTimeout(() => {
      fileElement.style.background = "";
    }, 1000);
  }

  uploadProgressCallback = (filename, finished, speed) => {
    var idx = this.hasFile(filename);

    if (!idx) {
      this.files.push({
        name: filename,
        type: "uploading",
        finished: finished,
        speed: speed
      });
      return 0;
    }

    this.files[idx].finished = finished;
    this.files[idx].speed = speed;
    this.update();
  };
  uploadFinishedCallback = filename => {
    var idx = this.hasFile(filename);

    if (idx != -1) {
      this.files.pop(idx);
      this.files.push({
        name: filename,
        path: this.url + filename,
        type: "file"
      });
    }

    this.update();
    this.scrollToFile(filename);
  };

  render() {
    this.renderRoot.removeEventListener("contextmenu", this.contextmenu);
    this.renderRoot.addEventListener("contextmenu", this.contextmenu);
    this.onclick = this.menu.close;

    if (!this.files) {
      return;
    }

    if (!this.showHidden) {
      var files = this.files.filter(file => {
        if (file.name.startsWith(".")) {
          return false;
        }

        return true;
      });
    } else {
      var files = this.files;
    }

    var prev = this.url.split("/").slice(0, -2).join("/");

    if (this.url != "/") {
      prev = y`<a class="dir" href="#${this.urlRoot}/${prev}">../</a><br>`;
    } else {
      prev = y``;
    }

    return y`${this.menu} <strong>Path:${decodeURIComponent(this.url)}</strong><br><div>${prev} ${files.map(file => y`${o(file.type, [["dir", () => y`<a id="file-${file.name}" tc-filename="${file.name}" class="dir" href="#${cleanPath(this.urlRoot + "/" + this.url + "/" + file.name)}/">${file.name}/</a>`], ["broken", () => y`<a id="file-${file.name}" tc-filename="${file.name}" class="broken" href="${cleanPath(this.apiBase + "/" + this.url + "/" + file.name)}">${file.name}/</a>`], ["file", () => y`<a class="file" id="file-${file.name}" tc-filename="${file.name}" href="${cleanPath(this.apiBase + "/" + this.url + "/" + file.name)}" download="${file.name}">${file.name}</a>`], ["uploading", () => y`<a class="file" id="file-${file.name}" tc-filename="${file.name}" style="background-image:linear-gradient(to right,gray ${file.finished}%,var(--tc-background) ${file.finished}%)">${file.name}</a> - ${file.speed}`], ["mountpoint", () => y`<a class="mountpoint" id="file-${file.name}" tc-filename="${file.name}" href="#${cleanPath(this.urlRoot + "/" + this.url + "/" + file.name)}">${file.name}</a>`]])}<br>`)}</div>`;
  }

}
class tc_fileupload extends s {
  static properties = {
    url: {},
    uploadFinishedCallback: {},
    uploadProgressCallback: {},
    ol: {},
    apiBase: {}
  };
  static styles = i$1`div{width:20rem;height:10rem;border-style:solid}p{margin:4rem}`;

  constructor() {
    super();
    this.apiBase = "dav/";
  }

  upload_file(file) {
    var xhr = new XMLHttpRequest();
    xhr.open("PUT", this.apiBase + this.url + "/" + file.name + "/");

    xhr.onload = () => {
      if (xhr.status == 200) {
        this.uploadFinishedCallback(file.name);
      }
    };

    xhr.upload.onprogress = e => {
      var nt = new Date().getTime(); //获取当前时间

      var pertime = (nt - ot) / 1000; //计算出上次调用该方法时到现在的时间差，单位为s

      ot = new Date().getTime(); //重新赋值时间，用于下次计算

      var perload = e.loaded - this.ol; //计算该分段上传的文件大小，单位b

      this.ol = e.loaded; //重新赋值已上传文件大小，用以下次计算
      //上传速度计算

      var speed = perload / pertime; //单位b/s
      var units = "b/s"; //单位名称

      if (speed / 1024 > 1) {
        speed = speed / 1024;
        units = "k/s";
      }

      if (speed / 1024 > 1) {
        speed = speed / 1024;
        units = "M/s";
      }

      speed = speed.toFixed(1);
      this.uploadProgressCallback(file.name, Math.round(e.loaded / e.total * 100), speed + units);
      console.log(speed);
    };

    this.ol = 0; //设置上传开始时间

    var ot = new Date().getTime();
    xhr.send(file); //    fetch('/dav' + this.url + '/' + file.name, {
    //     method: 'PUT',
    //    body: file,
    // }).then(() => this.uploadCallback(file.name));
  }

  render() {
    this.drop = document.createElement("div");
    this.drop.innerHTML = "<p align='center'>Drop file in<p>";
    /*    this.drop.addEventListener(
      'dragenter',
      (e) => {
        e.preventDefault();
      },
      false
    );
    this.drop.addEventListener(
      'dragover',
      (e) => {
        e.preventDefault();
      },
      false
    ); */

    this.drop.addEventListener("drop", e => {
      e.preventDefault();
      this.upload_file(e.dataTransfer.files[0]);
    }, false);
    this.drop.addEventListener("click", () => this.input_form.click());
    this.input_form = document.createElement("input");
    this.input_form.type = "file";
    this.input_form.style.display = "none";

    this.input_form.onchange = e => {
      this.upload_file(this.input_form.files[0]);
    };

    return y`${this.drop}${this.input_form}`;
  }

}
customElements.define("tc-filelist", tc_filelist);
customElements.define("tc-fileupload", tc_fileupload);

export { setCookie as a, cleanPath as b, configureLocalization as c, tc_filelist as d, tc_fileupload as e, i$1 as i, msg as m, s, tc_shares as t, updateWhenLocaleChanges as u, y };
