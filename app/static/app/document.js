var $e=Object.defineProperty;var ke=(e,t,n)=>t in e?$e(e,t,{enumerable:!0,configurable:!0,writable:!0,value:n}):e[t]=n;var U=(e,t,n)=>(ke(e,typeof t!="symbol"?t+"":t,n),n);(function(){const t=document.createElement("link").relList;if(t&&t.supports&&t.supports("modulepreload"))return;for(const l of document.querySelectorAll('link[rel="modulepreload"]'))s(l);new MutationObserver(l=>{for(const i of l)if(i.type==="childList")for(const r of i.addedNodes)r.tagName==="LINK"&&r.rel==="modulepreload"&&s(r)}).observe(document,{childList:!0,subtree:!0});function n(l){const i={};return l.integrity&&(i.integrity=l.integrity),l.referrerPolicy&&(i.referrerPolicy=l.referrerPolicy),l.crossOrigin==="use-credentials"?i.credentials="include":l.crossOrigin==="anonymous"?i.credentials="omit":i.credentials="same-origin",i}function s(l){if(l.ep)return;l.ep=!0;const i=n(l);fetch(l.href,i)}})();function w(){}function me(e){return e()}function le(){return Object.create(null)}function I(e){e.forEach(me)}function _e(e){return typeof e=="function"}function A(e,t){return e!=e?t==t:e!==t||e&&typeof e=="object"||typeof e=="function"}function we(e){return Object.keys(e).length===0}function b(e,t){e.appendChild(t)}function N(e,t,n){e.insertBefore(t,n||null)}function E(e){e.parentNode&&e.parentNode.removeChild(e)}function X(e,t){for(let n=0;n<e.length;n+=1)e[n]&&e[n].d(t)}function y(e){return document.createElement(e)}function H(e){return document.createTextNode(e)}function S(){return H(" ")}function M(e,t,n,s){return e.addEventListener(t,n,s),()=>e.removeEventListener(t,n,s)}function G(e){return function(t){return t.preventDefault(),e.call(this,t)}}function $(e,t,n){n==null?e.removeAttribute(t):e.getAttribute(t)!==n&&e.setAttribute(t,n)}function Ee(e){return Array.from(e.childNodes)}function Z(e,t){t=""+t,e.data!==t&&(e.data=t)}function ie(e,t,n){e.classList.toggle(t,!!n)}function Ne(e,t,{bubbles:n=!1,cancelable:s=!1}={}){return new CustomEvent(e,{detail:t,bubbles:n,cancelable:s})}let D;function C(e){D=e}function ee(){if(!D)throw new Error("Function called outside component initialization");return D}function Se(e){ee().$$.on_mount.push(e)}function xe(e){ee().$$.on_destroy.push(e)}function pe(){const e=ee();return(t,n,{cancelable:s=!1}={})=>{const l=e.$$.callbacks[t];if(l){const i=Ne(t,n,{cancelable:s});return l.slice().forEach(r=>{r.call(e,i)}),!i.defaultPrevented}return!0}}function Oe(e,t){const n=e.$$.callbacks[t.type];n&&n.slice().forEach(s=>s.call(this,t))}const L=[],z=[];let j=[];const Q=[],Le=Promise.resolve();let W=!1;function Te(){W||(W=!0,Le.then(be))}function Y(e){j.push(e)}function ge(e){Q.push(e)}const V=new Set;let x=0;function be(){if(x!==0)return;const e=D;do{try{for(;x<L.length;){const t=L[x];x++,C(t),Me(t.$$)}}catch(t){throw L.length=0,x=0,t}for(C(null),L.length=0,x=0;z.length;)z.pop()();for(let t=0;t<j.length;t+=1){const n=j[t];V.has(n)||(V.add(n),n())}j.length=0}while(L.length);for(;Q.length;)Q.pop()();W=!1,V.clear(),C(e)}function Me(e){if(e.fragment!==null){e.update(),I(e.before_update);const t=e.dirty;e.dirty=[-1],e.fragment&&e.fragment.p(e.ctx,t),e.after_update.forEach(Y)}}function je(e){const t=[],n=[];j.forEach(s=>e.indexOf(s)===-1?t.push(s):n.push(s)),n.forEach(s=>s()),j=t}const B=new Set;let Ae;function R(e,t){e&&e.i&&(B.delete(e),e.i(t))}function te(e,t,n,s){if(e&&e.o){if(B.has(e))return;B.add(e),Ae.c.push(()=>{B.delete(e),s&&(n&&e.d(1),s())}),e.o(t)}else s&&s()}function T(e){return(e==null?void 0:e.length)!==void 0?e:Array.from(e)}function ve(e,t,n){const s=e.$$.props[t];s!==void 0&&(e.$$.bound[s]=n,n(e.$$.ctx[s]))}function ne(e){e&&e.c()}function J(e,t,n){const{fragment:s,after_update:l}=e.$$;s&&s.m(t,n),Y(()=>{const i=e.$$.on_mount.map(me).filter(_e);e.$$.on_destroy?e.$$.on_destroy.push(...i):I(i),e.$$.on_mount=[]}),l.forEach(Y)}function K(e,t){const n=e.$$;n.fragment!==null&&(je(n.after_update),I(n.on_destroy),n.fragment&&n.fragment.d(t),n.on_destroy=n.fragment=null,n.ctx=[])}function Ce(e,t){e.$$.dirty[0]===-1&&(L.push(e),Te(),e.$$.dirty.fill(0)),e.$$.dirty[t/31|0]|=1<<t%31}function P(e,t,n,s,l,i,r,f=[-1]){const m=D;C(e);const o=e.$$={fragment:null,ctx:[],props:i,update:w,not_equal:l,bound:le(),on_mount:[],on_destroy:[],on_disconnect:[],before_update:[],after_update:[],context:new Map(t.context||(m?m.$$.context:[])),callbacks:le(),dirty:f,skip_bound:!1,root:t.target||m.$$.root};r&&r(o.root);let v=!1;if(o.ctx=n?n(e,t.props||{},(c,a,...h)=>{const k=h.length?h[0]:a;return o.ctx&&l(o.ctx[c],o.ctx[c]=k)&&(!o.skip_bound&&o.bound[c]&&o.bound[c](k),v&&Ce(e,c)),a}):[],o.update(),v=!0,I(o.before_update),o.fragment=s?s(o.ctx):!1,t.target){if(t.hydrate){const c=Ee(t.target);o.fragment&&o.fragment.l(c),c.forEach(E)}else o.fragment&&o.fragment.c();t.intro&&R(e.$$.fragment),J(e,t.target,t.anchor),be()}C(m)}class q{constructor(){U(this,"$$");U(this,"$$set")}$destroy(){K(this,1),this.$destroy=w}$on(t,n){if(!_e(n))return w;const s=this.$$.callbacks[t]||(this.$$.callbacks[t]=[]);return s.push(n),()=>{const l=s.indexOf(n);l!==-1&&s.splice(l,1)}}$set(t){this.$$set&&!we(t)&&(this.$$.skip_bound=!0,this.$$set(t),this.$$.skip_bound=!1)}}const De="4";typeof window<"u"&&(window.__svelte||(window.__svelte={v:new Set})).v.add(De);const O=[];function Ie(e,t=w){let n;const s=new Set;function l(f){if(A(e,f)&&(e=f,n)){const m=!O.length;for(const o of s)o[1](),O.push(o,e);if(m){for(let o=0;o<O.length;o+=2)O[o][0](O[o+1]);O.length=0}}}function i(f){l(f(e))}function r(f,m=w){const o=[f,m];return s.add(o),s.size===1&&(n=t(l,i)||w),f(e),()=>{s.delete(o),s.size===0&&n&&(n(),n=null)}}return{set:l,update:i,subscribe:r}}const F=Ie(!1);function Pe(e){let t,n,s,l,i,r,f,m,o,v,c;return{c(){t=y("div"),n=y("div"),s=S(),l=y("div"),i=y("form"),r=y("div"),f=y("div"),m=S(),o=y("div"),o.innerHTML='<p class="control"><button type="submit" class="button is-success svelte-1vm7l7d" title="Подтвердить"><span class="icon is-small"><i class="fa-light fa-check"></i></span><span>Да</span></button></p> <p class="control"><button type="reset" class="button is-danger is-outlined svelte-1vm7l7d" title="Отменить"><span class="icon is-small"><i class="fa-light fa-xmark"></i></span><span>Нет</span></button></p>',$(n,"class","modal-background"),$(f,"class","container content"),$(o,"class","field is-grouped is-grouped-centered"),$(r,"class","message-body"),$(i,"class","message is-warning"),$(l,"class","modal-content"),$(t,"class","modal"),ie(t,"is-active",e[0])},m(a,h){N(a,t,h),b(t,n),b(t,s),b(t,l),b(l,i),b(i,r),b(r,f),f.innerHTML=e[1],b(r,m),b(r,o),v||(c=[M(n,"click",e[3]),M(i,"submit",G(e[2])),M(i,"reset",G(e[3]))],v=!0)},p(a,[h]){h&2&&(f.innerHTML=a[1]),h&1&&ie(t,"is-active",a[0])},i:w,o:w,d(a){a&&E(t),v=!1,I(c)}}}let ce="modalevent";function qe(e,t,n){const s=pe();let{htmldata:l="Sample modal data"}=t,{active:i=!1}=t,r=!1;const f=()=>{r=!0,n(0,i=!1),s(ce,r)},m=()=>{r=!1,n(0,i=!1),s(ce,r)};return e.$$set=o=>{"htmldata"in o&&n(1,l=o.htmldata),"active"in o&&n(0,i=o.active)},[i,l,f,m]}class Be extends q{constructor(t){super(),P(this,t,qe,Pe,A,{htmldata:1,active:0})}}function ze(e){let t,n,s,l,i,r,f,m,o;function v(a){e[4](a)}let c={htmldata:Fe};return e[1]!==void 0&&(c.active=e[1]),i=new Be({props:c}),z.push(()=>ve(i,"active",v)),i.$on("modalevent",e[3]),{c(){t=y("button"),n=y("i"),l=S(),ne(i.$$.fragment),$(n,"class","fa-light fa-trash-xmark"),$(t,"type","submit"),$(t,"class","button is-link is-outlined mt-1 ml-2"),t.disabled=s=!e[0],$(t,"title","Удалить отмеченные")},m(a,h){N(a,t,h),b(t,n),N(a,l,h),J(i,a,h),f=!0,m||(o=M(t,"click",G(e[2])),m=!0)},p(a,[h]){(!f||h&1&&s!==(s=!a[0]))&&(t.disabled=s);const k={};!r&&h&2&&(r=!0,k.active=a[1],ge(()=>r=!1)),i.$set(k)},i(a){f||(R(i.$$.fragment,a),f=!0)},o(a){te(i.$$.fragment,a),f=!1},d(a){a&&(E(t),E(l)),K(i,a),m=!1,o()}}}let Fe="<p>Удаление <span class='has-text-danger-dark'>необратимо</span>! Удалить?</p>";const He="notification";function Re(e,t,n){const s=document.querySelector("[name=csrfmiddlewaretoken]").value,l="https://"+document.domain+app.dataset.api;let i=!1;const r=pe();let{disabled:f=!0}=t,m=F.subscribe(_=>n(0,f=_));xe(m);const o={add_class:"is-danger",text:"Не удалось удалить:"};let v=null;const c=_=>{v=_.currentTarget,n(1,i=!0)};async function a(_){if(!_.detail)return;const u=v.parentElement;let p="";const d=new FormData(u);for(let g of d.values())p+=await h(g);if(r("deleteitem"),p){let g={...o};g.text+=p,r(He,g)}F.update(g=>!1)}const h=async _=>{try{const u=await fetch(`${l}${_}/`,{method:"delete",headers:{"X-CSRFToken":s}});return u.ok?"":`<br> id: ${_}, ${u.status} - ${u.statusText}`}catch(u){return`<br> id: ${_}, ${u.message}`}};function k(_){i=_,n(1,i)}return e.$$set=_=>{"disabled"in _&&n(0,f=_.disabled)},[f,i,c,a,k]}class Je extends q{constructor(t){super(),P(this,t,Re,ze,A,{disabled:0})}}function re(e,t,n){const s=e.slice();s[8]=t[n];const l=Object.values(s[8]);return s[9]=l,s}function oe(e,t,n){const s=e.slice();return s[12]=t[n],s}function ae(e,t,n){const s=e.slice();return s[15]=t[n],s}function ue(e){let t,n=e[5](e[15])+"",s;return{c(){t=y("th"),s=H(n),$(t,"class","has-text-grey svelte-5f7ih4")},m(l,i){N(l,t,i),b(t,s)},p(l,i){i&1&&n!==(n=l[5](l[15])+"")&&Z(s,n)},d(l){l&&E(t)}}}function fe(e){let t,n=e[12]+"",s;return{c(){t=y("td"),s=H(n)},m(l,i){N(l,t,i),b(t,s)},p(l,i){i&1&&n!==(n=l[12]+"")&&Z(s,n)},d(l){l&&E(t)}}}function de(e){let t,n,s,l,i,r,f,m=e[9][1]+"",o,v,c,a,h,k,_=T(e[9].slice(2)),u=[];for(let p=0;p<_.length;p+=1)u[p]=fe(oe(e,_,p));return{c(){t=y("tr"),n=y("td"),s=y("input"),i=S(),r=y("td"),f=y("a"),o=H(m),c=S();for(let p=0;p<u.length;p+=1)u[p].c();a=S(),$(s,"type","checkbox"),$(s,"name",e[2]),s.value=l=e[9][0],$(f,"href",v=""+(e[1]+e[9][0])),$(f,"class","svelte-5f7ih4")},m(p,d){N(p,t,d),b(t,n),b(n,s),b(t,i),b(t,r),b(r,f),b(f,o),b(t,c);for(let g=0;g<u.length;g+=1)u[g]&&u[g].m(t,null);b(t,a),h||(k=M(s,"change",e[3]),h=!0)},p(p,d){if(d&4&&$(s,"name",p[2]),d&1&&l!==(l=p[9][0])&&(s.value=l),d&1&&m!==(m=p[9][1]+"")&&Z(o,m),d&3&&v!==(v=""+(p[1]+p[9][0]))&&$(f,"href",v),d&1){_=T(p[9].slice(2));let g;for(g=0;g<_.length;g+=1){const se=oe(p,_,g);u[g]?u[g].p(se,d):(u[g]=fe(se),u[g].c(),u[g].m(t,a))}for(;g<u.length;g+=1)u[g].d(1);u.length=_.length}},d(p){p&&E(t),X(u,p),h=!1,k()}}}function Ke(e){let t,n,s,l,i,r,f,m,o,v,c,a=T(Object.keys(e[0][0]).slice(1)),h=[];for(let u=0;u<a.length;u+=1)h[u]=ue(ae(e,a,u));let k=T(e[0]),_=[];for(let u=0;u<k.length;u+=1)_[u]=de(re(e,k,u));return{c(){t=y("div"),n=y("table"),s=y("thead"),l=y("tr"),i=y("th"),r=y("input"),f=S();for(let u=0;u<h.length;u+=1)h[u].c();m=S(),o=y("tbody");for(let u=0;u<_.length;u+=1)_[u].c();$(r,"type","checkbox"),$(r,"id",ye),$(i,"class","svelte-5f7ih4"),$(n,"class","table is-hoverable is-striped has-background-white-ter"),$(t,"class","svelte-5f7ih4")},m(u,p){N(u,t,p),b(t,n),b(n,s),b(s,l),b(l,i),b(i,r),b(l,f);for(let d=0;d<h.length;d+=1)h[d]&&h[d].m(l,null);b(n,m),b(n,o);for(let d=0;d<_.length;d+=1)_[d]&&_[d].m(o,null);v||(c=M(r,"change",e[4]),v=!0)},p(u,[p]){if(p&33){a=T(Object.keys(u[0][0]).slice(1));let d;for(d=0;d<a.length;d+=1){const g=ae(u,a,d);h[d]?h[d].p(g,p):(h[d]=ue(g),h[d].c(),h[d].m(l,null))}for(;d<h.length;d+=1)h[d].d(1);h.length=a.length}if(p&15){k=T(u[0]);let d;for(d=0;d<k.length;d+=1){const g=re(u,k,d);_[d]?_[d].p(g,p):(_[d]=de(g),_[d].c(),_[d].m(o,null))}for(;d<_.length;d+=1)_[d].d(1);_.length=k.length}},i:w,o:w,d(u){u&&E(t),X(h,u),X(_,u),v=!1,c()}}}const Ue="has-background-warning-light",ye="tablegen-all";function Ve(e,t,n){let{table_content:s=[]}=t,{href:l="/item/"}=t,{checkbox_name:i="id"}=t;const r=new Set;function f(c){let a=c.currentTarget;m(a)}const m=c=>{c.checked?(r.add(c.value),F.update(a=>!0),c.parentNode.parentNode.className=Ue):(document.querySelector(`#${ye}`).checked=!1,r.delete(c.value),r.size==0&&F.update(a=>!1),c.parentNode.parentNode.className="")},o=c=>{let a=c.currentTarget,h=document.getElementsByName(i);if(a.checked)for(let k of h)k.checked=!0,m(k);else for(let k of h)k.checked=!1,m(k)},v=c=>{const a={name:"Наименование",address:"Адрес",inn:"ИНН",kpp:"КПП",ogrn:"ОГРН",bank:"Банк",bik:"БИК",pay_acount:"Номер счёта",kor_acount:"Корр. счёт",phone:"Телефон",number:"Номер",data:"Дата",city:"Город",truck:"Номер машины",spec_notes:"Особые отметки",destination_address:"Адрес назначения",text:"Условия договора",sender:"Отправитель",receiver:"Получатель",payer:"Плательщик"};return c=a[c]?a[c]:c,c};return e.$$set=c=>{"table_content"in c&&n(0,s=c.table_content),"href"in c&&n(1,l=c.href),"checkbox_name"in c&&n(2,i=c.checkbox_name)},[s,l,i,f,o,v]}class Xe extends q{constructor(t){super(),P(this,t,Ve,Ke,A,{table_content:0,href:1,checkbox_name:2})}}function Ge(e){let t,n,s,l,i,r,f,m;function o(c){e[3](c)}let v={};return e[0]!==void 0&&(v.disabled=e[0]),r=new Je({props:v}),z.push(()=>ve(r,"disabled",o)),r.$on("notification",e[4]),r.$on("deleteitem",e[2]),{c(){t=y("h4"),t.textContent="Список документов.",n=S(),s=y("form"),l=y("div"),i=S(),ne(r.$$.fragment),$(t,"class","title is-4 pl-4 pt-5"),$(l,"id",e[1])},m(c,a){N(c,t,a),N(c,n,a),N(c,s,a),b(s,l),b(s,i),J(r,s,null),m=!0},p(c,[a]){const h={};!f&&a&1&&(f=!0,h.disabled=c[0],ge(()=>f=!1)),r.$set(h)},i(c){m||(R(r.$$.fragment,c),m=!0)},o(c){te(r.$$.fragment,c),m=!1},d(c){c&&(E(t),E(n),E(s)),K(r)}}}const Qe="/document/";function he(e){let t=JSON.parse(JSON.stringify(e,["id","number","data","city","truck","destination_address"]));for(let n=0;n<t.length;n++)t[n].sender=e[n].sender.name,t[n].receiver=e[n].receiver.name,t[n].payer=e[n].payer.name;return t}function We(e,t){return e.id<t.id?1:e.id>t.id?-1:0}function Ye(e,t,n){let s=!0;const l="https://"+document.domain+app.dataset.api;let i,r=[];const f="tablegen_"+Math.round(Math.random()*1e4),m=async()=>{r=await fetch(l).then(c=>c.json()),i==null||i.$destroy(),i=new Xe({target:document.getElementById(f),props:{table_content:he(r).sort(We),href:Qe,checkbox_name:"id"}}),he(r)};Se(m),document.querySelector("#navbar-item-documents").classList.add("is-active");function o(c){s=c,n(0,s)}function v(c){Oe.call(this,e,c)}return[s,f,m,o,v]}class Ze extends q{constructor(t){super(),P(this,t,Ye,Ge,A,{})}}function et(e){let t,n;return t=new Ze({}),{c(){ne(t.$$.fragment)},m(s,l){J(t,s,l),n=!0},p:w,i(s){n||(R(t.$$.fragment,s),n=!0)},o(s){te(t.$$.fragment,s),n=!1},d(s){K(t,s)}}}class tt extends q{constructor(t){super(),P(this,t,null,et,A,{})}}new tt({target:document.getElementById("app")});
