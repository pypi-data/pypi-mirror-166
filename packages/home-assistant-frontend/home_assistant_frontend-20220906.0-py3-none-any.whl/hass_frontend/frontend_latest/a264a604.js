"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[50850],{19267:(e,t,i)=>{i.a(e,(async e=>{var t=i(37500),r=i(33310),n=i(47181),o=(i(13266),i(22098),i(31206),i(4940),i(3555),i(25727)),s=(i(14089),i(86490)),a=i(11654),l=(i(88165),e([o]));function c(){c=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!u(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return y(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?y(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=m(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:f(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=f(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function d(e){var t,i=m(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function h(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function u(e){return e.decorators&&e.decorators.length}function p(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function f(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function m(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function y(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function v(e,t,i){return v="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=g(e)););return e}(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(i):n.value}},v(e,t,i||e)}function g(e){return g=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},g(e)}o=(l.then?await l:l)[0];!function(e,t,i,r){var n=c();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),i),a=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(p(o.descriptor)||p(n.descriptor)){if(u(o)||u(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(u(o)){if(u(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}h(o,n)}else t.push(o)}return t}(s.d.map(d)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,r.Mo)("blueprint-script-editor")],(function(e,i){class o extends i{constructor(...t){super(...t),e(this)}}return{F:o,d:[{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"isWide",value:void 0},{kind:"field",decorators:[(0,r.Cb)({reflect:!0,type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"config",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_blueprints",value:void 0},{kind:"method",key:"firstUpdated",value:function(e){v(g(o.prototype),"firstUpdated",this).call(this,e),this._getBlueprints()}},{kind:"get",key:"_blueprint",value:function(){if(this._blueprints)return this._blueprints[this.config.use_blueprint.path]}},{kind:"method",key:"render",value:function(){var e;const i=this._blueprint;return t.dy` <ha-config-section vertical .isWide=${this.isWide}>
      <span slot="header"
        >${this.hass.localize("ui.panel.config.automation.editor.blueprint.header")}</span
      >
      <ha-card outlined>
        <div class="blueprint-picker-container">
          ${this._blueprints?Object.keys(this._blueprints).length?t.dy`
                  <ha-blueprint-picker
                    .hass=${this.hass}
                    .label=${this.hass.localize("ui.panel.config.automation.editor.blueprint.blueprint_to_use")}
                    .blueprints=${this._blueprints}
                    .value=${this.config.use_blueprint.path}
                    @value-changed=${this._blueprintChanged}
                  ></ha-blueprint-picker>
                `:this.hass.localize("ui.panel.config.automation.editor.blueprint.no_blueprints"):t.dy`<ha-circular-progress active></ha-circular-progress>`}
        </div>

        ${this.config.use_blueprint.path?i&&"error"in i?t.dy`<p class="warning padding">
                There is an error in this Blueprint: ${i.error}
              </p>`:t.dy`${null!=i&&i.metadata.description?t.dy`<ha-markdown
                    class="card-content"
                    breaks
                    .content=${i.metadata.description}
                  ></ha-markdown>`:""}
              ${null!=i&&null!==(e=i.metadata)&&void 0!==e&&e.input&&Object.keys(i.metadata.input).length?Object.entries(i.metadata.input).map((([e,i])=>{var r,n;return t.dy`<ha-settings-row .narrow=${this.narrow}>
                        <span slot="heading">${(null==i?void 0:i.name)||e}</span>
                        <span slot="description">${null==i?void 0:i.description}</span>
                        ${null!=i&&i.selector?t.dy`<ha-selector
                              .hass=${this.hass}
                              .selector=${i.selector}
                              .key=${e}
                              .value=${null!==(r=this.config.use_blueprint.input&&this.config.use_blueprint.input[e])&&void 0!==r?r:null==i?void 0:i.default}
                              @value-changed=${this._inputChanged}
                            ></ha-selector>`:t.dy`<ha-textfield
                              .key=${e}
                              required
                              .value=${null!==(n=this.config.use_blueprint.input&&this.config.use_blueprint.input[e])&&void 0!==n?n:null==i?void 0:i.default}
                              @change=${this._inputChanged}
                            ></ha-textfield>`}
                      </ha-settings-row>`})):t.dy`<p class="padding">
                    ${this.hass.localize("ui.panel.config.automation.editor.blueprint.no_inputs")}
                  </p>`}`:""}
      </ha-card>
    </ha-config-section>`}},{kind:"method",key:"_getBlueprints",value:async function(){this._blueprints=await(0,s.wc)(this.hass,"script")}},{kind:"method",key:"_blueprintChanged",value:function(e){e.stopPropagation(),this.config.use_blueprint.path!==e.detail.value&&(0,n.B)(this,"value-changed",{value:{...this.config,use_blueprint:{path:e.detail.value}}})}},{kind:"method",key:"_inputChanged",value:function(e){var t,i;e.stopPropagation();const r=e.target,o=r.key,s=null!==(t=null===(i=e.detail)||void 0===i?void 0:i.value)&&void 0!==t?t:r.value;if(this.config.use_blueprint.input&&this.config.use_blueprint.input[o]===s||!this.config.use_blueprint.input&&""===s)return;const a={...this.config.use_blueprint.input,[o]:s};""!==s&&void 0!==s||delete a[o],(0,n.B)(this,"value-changed",{value:{...this.config,use_blueprint:{...this.config.use_blueprint,input:a}}})}},{kind:"get",static:!0,key:"styles",value:function(){return[a.Qx,t.iv`
        .padding {
          padding: 16px;
        }
        .blueprint-picker-container {
          padding: 16px;
        }
        p {
          margin-bottom: 0;
        }
        ha-settings-row {
          --paper-time-input-justify-content: flex-end;
          border-top: 1px solid var(--divider-color);
        }
        :host(:not([narrow])) ha-settings-row ha-textfield,
        :host(:not([narrow])) ha-settings-row ha-selector {
          width: 60%;
        }
      `]}}]}}),t.oi)}))},50850:(e,t,i)=>{i.a(e,(async e=>{i.r(t);var r=i(33310),n=i(14516),o=i(22311),s=i(38346),a=i(18199),l=i(67826),c=i(25931),d=e([c,l]);function h(){h=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!f(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return g(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?g(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=v(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:y(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=y(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function u(e){var t,i=v(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function p(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function f(e){return e.decorators&&e.decorators.length}function m(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function y(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function v(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function g(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function b(e,t,i){return b="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=k(e)););return e}(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(i):n.value}},b(e,t,i||e)}function k(e){return k=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},k(e)}[c,l]=d.then?await d:d;!function(e,t,i,r){var n=h();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),i),a=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(m(o.descriptor)||m(n.descriptor)){if(f(o)||f(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(f(o)){if(f(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}p(o,n)}else t.push(o)}return t}(s.d.map(u)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,r.Mo)("ha-config-script")],(function(e,t){class a extends t{constructor(...t){super(...t),e(this)}}return{F:a,d:[{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"narrow",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"isWide",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"showAdvanced",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"scripts",value:()=>[]},{kind:"field",key:"routerOptions",value:()=>({defaultPage:"dashboard",routes:{dashboard:{tag:"ha-script-picker",cache:!0},edit:{tag:"ha-script-editor"},trace:{tag:"ha-script-trace",load:()=>Promise.all([i.e(99528),i.e(74790),i.e(15101)]).then(i.bind(i,67876))}}})},{kind:"field",key:"_debouncedUpdateScripts",value(){return(0,s.D)((e=>{const t=this._getScripts(this.hass.states);var i,r;i=t,r=e.scripts,i.length===r.length&&i.every(((e,t)=>e===r[t]))||(e.scripts=t)}),10)}},{kind:"field",key:"_getScripts",value:()=>(0,n.Z)((e=>Object.values(e).filter((e=>"script"===(0,o.N)(e)))))},{kind:"method",key:"firstUpdated",value:function(e){b(k(a.prototype),"firstUpdated",this).call(this,e),this.hass.loadBackendTranslation("device_automation")}},{kind:"method",key:"updatePageEl",value:function(e,t){if(e.hass=this.hass,e.narrow=this.narrow,e.isWide=this.isWide,e.route=this.routeTail,e.showAdvanced=this.showAdvanced,this.hass&&(e.scripts&&t?t.has("hass")&&this._debouncedUpdateScripts(e):e.scripts=this._getScripts(this.hass.states)),(!t||t.has("route"))&&"dashboard"!==this._currentPage){e.creatingNew=void 0;const t=this.routeTail.path.substr(1);e.scriptEntityId="new"===t?null:t}}}]}}),a.n)}))},67826:(e,t,i)=>{i.a(e,(async e=>{i(44577),i(53268),i(12730);var t=i(37500),r=i(33310),n=i(8636),o=i(14516),s=i(27269),a=i(83849),l=i(83447),c=i(87744),d=i(50577),h=(i(81545),i(22098),i(36125),i(10983),i(52039),i(18900),i(44547)),u=i(26765),p=(i(27849),i(60010),i(23670)),f=i(11654),m=i(27322),y=i(81796),v=i(43547),g=i(19267),b=e([g]);function k(){k=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!E(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return z(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?z(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=A(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:C(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=C(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function w(e){var t,i=A(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function _(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function E(e){return e.decorators&&e.decorators.length}function $(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function C(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function A(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function z(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function P(e,t,i){return P="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=x(e)););return e}(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(i):n.value}},P(e,t,i||e)}function x(e){return x=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},x(e)}g=(b.then?await b:b)[0];const S="M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z";let D=function(e,t,i,r){var n=k();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),i),a=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if($(o.descriptor)||$(n.descriptor)){if(E(o)||E(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(E(o)){if(E(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}_(o,n)}else t.push(o)}return t}(s.d.map(w)),e);return n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}(null,(function(e,i){class p extends i{constructor(...t){super(...t),e(this)}}return{F:p,d:[{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"scriptEntityId",value:()=>null},{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"route",value:void 0},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"isWide",value:()=>!1},{kind:"field",decorators:[(0,r.Cb)({type:Boolean})],key:"narrow",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_config",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_entityId",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_idError",value:()=>!1},{kind:"field",decorators:[(0,r.SB)()],key:"_dirty",value:()=>!1},{kind:"field",decorators:[(0,r.SB)()],key:"_errors",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_mode",value:()=>"gui"},{kind:"field",decorators:[(0,r.IO)("ha-yaml-editor",!0)],key:"_editor",value:void 0},{kind:"field",key:"_schema",value(){return(0,o.Z)(((e,t,i)=>[{name:"alias",selector:{text:{type:"text"}}},{name:"icon",selector:{icon:{}}},...e?[]:[{name:"id",selector:{text:{}}}],...t?[]:[{name:"mode",selector:{select:{mode:"dropdown",options:h.EH.map((e=>({label:this.hass.localize(`ui.panel.config.script.editor.modes.${e}`),value:e})))}}}],...i&&(0,h.vA)(i)?[{name:"max",required:!0,selector:{number:{mode:"box",min:1,max:1/0}}}]:[]]))}},{kind:"method",key:"render",value:function(){var e,i;if(!this._config)return t.dy``;const r=this._schema(!!this.scriptEntityId,"use_blueprint"in this._config,this._config.mode),o={mode:h.EH[0],icon:void 0,max:this._config.mode&&(0,h.vA)(this._config.mode)?10:void 0,...this._config,id:this._entityId};return t.dy`
      <hass-subpage
        .hass=${this.hass}
        .narrow=${this.narrow}
        .route=${this.route}
        .backCallback=${this._backTapped}
        .header=${null!==(e=this._config)&&void 0!==e&&e.alias?this._config.alias:""}
      >
        <ha-button-menu
          corner="BOTTOM_START"
          slot="toolbar-icon"
          @action=${this._handleMenuAction}
          activatable
        >
          <ha-icon-button
            slot="trigger"
            .label=${this.hass.localize("ui.common.menu")}
            .path=${"M12,16A2,2 0 0,1 14,18A2,2 0 0,1 12,20A2,2 0 0,1 10,18A2,2 0 0,1 12,16M12,10A2,2 0 0,1 14,12A2,2 0 0,1 12,14A2,2 0 0,1 10,12A2,2 0 0,1 12,10M12,4A2,2 0 0,1 14,6A2,2 0 0,1 12,8A2,2 0 0,1 10,6A2,2 0 0,1 12,4Z"}
          ></ha-icon-button>

          <mwc-list-item
            aria-label=${this.hass.localize("ui.panel.config.automation.editor.edit_ui")}
            graphic="icon"
          >
            ${this.hass.localize("ui.panel.config.automation.editor.edit_ui")}
            ${"gui"===this._mode?t.dy`
                  <ha-svg-icon
                    class="selected_menu_item"
                    slot="graphic"
                    .path=${S}
                  ></ha-svg-icon>
                `:""}
          </mwc-list-item>
          <mwc-list-item
            aria-label=${this.hass.localize("ui.panel.config.automation.editor.edit_yaml")}
            graphic="icon"
          >
            ${this.hass.localize("ui.panel.config.automation.editor.edit_yaml")}
            ${"yaml"===this._mode?t.dy`
                  <ha-svg-icon
                    class="selected_menu_item"
                    slot="graphic"
                    .path=${S}
                  ></ha-svg-icon>
                `:""}
          </mwc-list-item>

          <li divider role="separator"></li>

          <mwc-list-item
            .disabled=${!this.scriptEntityId}
            .label=${this.hass.localize("ui.panel.config.script.picker.duplicate")}
            graphic="icon"
          >
            ${this.hass.localize("ui.panel.config.script.picker.duplicate")}
            <ha-svg-icon
              slot="graphic"
              .path=${"M11,17H4A2,2 0 0,1 2,15V3A2,2 0 0,1 4,1H16V3H4V15H11V13L15,16L11,19V17M19,21V7H8V13H6V7A2,2 0 0,1 8,5H19A2,2 0 0,1 21,7V21A2,2 0 0,1 19,23H8A2,2 0 0,1 6,21V19H8V21H19Z"}
            ></ha-svg-icon>
          </mwc-list-item>

          <mwc-list-item
            .disabled=${!this.scriptEntityId}
            aria-label=${this.hass.localize("ui.panel.config.script.picker.delete")}
            class=${(0,n.$)({warning:Boolean(this.scriptEntityId)})}
            graphic="icon"
          >
            ${this.hass.localize("ui.panel.config.script.picker.delete")}
            <ha-svg-icon
              class=${(0,n.$)({warning:Boolean(this.scriptEntityId)})}
              slot="graphic"
              .path=${"M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z"}
            >
            </ha-svg-icon>
          </mwc-list-item>
        </ha-button-menu>
        <div
          class="content ${(0,n.$)({"yaml-mode":"yaml"===this._mode})}"
        >
          ${this._errors?t.dy`<div class="errors">${this._errors}</div>`:""}
          ${"gui"===this._mode?t.dy`
                <div
                  class=${(0,n.$)({rtl:(0,c.HE)(this.hass)})}
                >
                  ${this._config?t.dy`
                        <ha-card outlined>
                          <div class="card-content">
                            <ha-form
                              .schema=${r}
                              .data=${o}
                              .hass=${this.hass}
                              .computeLabel=${this._computeLabelCallback}
                              .computeHelper=${this._computeHelperCallback}
                              @value-changed=${this._valueChanged}
                            ></ha-form>
                          </div>
                          ${this.scriptEntityId?t.dy`
                                <div
                                  class="card-actions layout horizontal justified center"
                                >
                                  <a
                                    href="/config/script/trace/${this.scriptEntityId}"
                                  >
                                    <mwc-button>
                                      ${this.hass.localize("ui.panel.config.script.editor.show_trace")}
                                    </mwc-button>
                                  </a>
                                  <mwc-button
                                    @click=${this._runScript}
                                    title=${this.hass.localize("ui.panel.config.script.picker.run_script")}
                                    ?disabled=${this._dirty}
                                  >
                                    ${this.hass.localize("ui.panel.config.script.picker.run_script")}
                                  </mwc-button>
                                </div>
                              `:""}
                        </ha-card>

                        ${"use_blueprint"in this._config?t.dy`
                              <blueprint-script-editor
                                .hass=${this.hass}
                                .narrow=${this.narrow}
                                .isWide=${this.isWide}
                                .config=${this._config}
                                @value-changed=${this._configChanged}
                              ></blueprint-script-editor>
                            `:t.dy`
                              <div class="header">
                                <h2 id="sequence-heading" class="name">
                                  ${this.hass.localize("ui.panel.config.script.editor.sequence")}
                                </h2>
                                <a
                                  href=${(0,m.R)(this.hass,"/docs/scripts/")}
                                  target="_blank"
                                  rel="noreferrer"
                                >
                                  <ha-icon-button
                                    .path=${"M15.07,11.25L14.17,12.17C13.45,12.89 13,13.5 13,15H11V14.5C11,13.39 11.45,12.39 12.17,11.67L13.41,10.41C13.78,10.05 14,9.55 14,9C14,7.89 13.1,7 12,7A2,2 0 0,0 10,9H8A4,4 0 0,1 12,5A4,4 0 0,1 16,9C16,9.88 15.64,10.67 15.07,11.25M13,19H11V17H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12C22,6.47 17.5,2 12,2Z"}
                                    .label=${this.hass.localize("ui.panel.config.script.editor.link_available_actions")}
                                  ></ha-icon-button>
                                </a>
                              </div>

                              <ha-automation-action
                                role="region"
                                aria-labelledby="sequence-heading"
                                .actions=${this._config.sequence}
                                @value-changed=${this._sequenceChanged}
                                .hass=${this.hass}
                              ></ha-automation-action>
                            `}
                      `:""}
                </div>
              `:"yaml"===this._mode?t.dy`
                ${this.narrow?"":t.dy`
                      <ha-card outlined>
                        <div class="card-header">${null===(i=this._config)||void 0===i?void 0:i.alias}</div>
                        <div
                          class="card-actions layout horizontal justified center"
                        >
                          <mwc-button
                            @click=${this._runScript}
                            title=${this.hass.localize("ui.panel.config.script.picker.run_script")}
                            ?disabled=${this._dirty}
                          >
                            ${this.hass.localize("ui.panel.config.script.picker.run_script")}
                          </mwc-button>
                        </div>
                      </ha-card>
                    `}
                <ha-yaml-editor
                  .hass=${this.hass}
                  .defaultValue=${this._preprocessYaml()}
                  @value-changed=${this._yamlChanged}
                ></ha-yaml-editor>
                <ha-card outlined>
                  <div class="card-actions">
                    <mwc-button @click=${this._copyYaml}>
                      ${this.hass.localize("ui.panel.config.automation.editor.copy_to_clipboard")}
                    </mwc-button>
                  </div>
                </ha-card>
              `:""}
        </div>
        <ha-fab
          slot="fab"
          .label=${this.hass.localize("ui.panel.config.script.editor.save_script")}
          extended
          @click=${this._saveScript}
          class=${(0,n.$)({dirty:this._dirty})}
        >
          <ha-svg-icon slot="icon" .path=${"M15,9H5V5H15M12,19A3,3 0 0,1 9,16A3,3 0 0,1 12,13A3,3 0 0,1 15,16A3,3 0 0,1 12,19M17,3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V7L17,3Z"}></ha-svg-icon>
        </ha-fab>
      </hass-subpage>
    `}},{kind:"method",key:"updated",value:function(e){P(x(p.prototype),"updated",this).call(this,e);const t=e.get("scriptEntityId");if(e.has("scriptEntityId")&&this.scriptEntityId&&this.hass&&(!t||t!==this.scriptEntityId)&&(0,h.Vn)(this.hass,(0,s.p)(this.scriptEntityId)).then((e=>{const t=e.sequence;t&&!Array.isArray(t)&&(e.sequence=[t]),this._dirty=!1,this._config=e}),(e=>{alert(404===e.status_code?this.hass.localize("ui.panel.config.script.editor.load_error_not_editable"):this.hass.localize("ui.panel.config.script.editor.load_error_unknown","err_no",e.status_code)),history.back()})),e.has("scriptEntityId")&&!this.scriptEntityId&&this.hass){const e=(0,h.FI)();this._dirty=!!e;const t={alias:this.hass.localize("ui.panel.config.script.editor.default_name")};e&&"use_blueprint"in e||(t.sequence=[{...v.x.defaultConfig}]),this._config={...t,...e}}}},{kind:"field",key:"_computeLabelCallback",value(){return(e,t)=>{switch(e.name){case"mode":return this.hass.localize("ui.panel.config.script.editor.modes.label");case"max":return this.hass.localize(`ui.panel.config.script.editor.max.${t.mode}`);default:return this.hass.localize(`ui.panel.config.script.editor.${e.name}`)}}}},{kind:"field",key:"_computeHelperCallback",value(){return e=>{if("mode"===e.name)return t.dy`
        <a
          style="color: var(--secondary-text-color)"
          href=${(0,m.R)(this.hass,"/integrations/script/#script-modes")}
          target="_blank"
          rel="noreferrer"
          >${this.hass.localize("ui.panel.config.script.editor.modes.learn_more")}</a
        >
      `}}},{kind:"method",key:"_runScript",value:async function(e){e.stopPropagation(),await(0,h.kC)(this.hass,this.scriptEntityId),(0,y.C)(this,{message:this.hass.localize("ui.notification_toast.triggered","name",this._config.alias)})}},{kind:"method",key:"_modeChanged",value:function(e){e!==(this._config.mode||h.EH[0])&&(this._config={...this._config,mode:e},(0,h.vA)(e)||delete this._config.max,this._dirty=!0)}},{kind:"method",key:"_aliasChanged",value:function(e){if(this.scriptEntityId||this._entityId&&this._entityId!==(0,l.l)(this._config.alias))return;const t=(0,l.l)(e);let i=t,r=2;for(;this.hass.states[`script.${i}`];)i=`${t}_${r}`,r++;this._entityId=i}},{kind:"method",key:"_idChanged",value:function(e){this._entityId=e,this.hass.states[`script.${this._entityId}`]?this._idError=!0:this._idError=!1}},{kind:"method",key:"_valueChanged",value:function(e){e.stopPropagation();const t=e.detail.value,i=this._entityId;let r=!1;for(const e of Object.keys(t)){if("sequence"===e)continue;const n=t[e];if(n!==this._config[e]&&("id"!==e||i!==n)){switch(r=!0,e){case"id":return void this._idChanged(n);case"alias":this._aliasChanged(n);break;case"mode":return void this._modeChanged(n)}if(void 0===t[e]){const t={...this._config};delete t[e],this._config=t}else this._config={...this._config,[e]:n}}}r&&(this._dirty=!0)}},{kind:"method",key:"_configChanged",value:function(e){this._config=e.detail.value,this._dirty=!0}},{kind:"method",key:"_sequenceChanged",value:function(e){this._config={...this._config,sequence:e.detail.value},this._errors=void 0,this._dirty=!0}},{kind:"method",key:"_preprocessYaml",value:function(){return this._config}},{kind:"method",key:"_copyYaml",value:async function(){var e;null!==(e=this._editor)&&void 0!==e&&e.yaml&&(await(0,d.v)(this._editor.yaml),(0,y.C)(this,{message:this.hass.localize("ui.common.copied_clipboard")}))}},{kind:"method",key:"_yamlChanged",value:function(e){e.stopPropagation(),e.detail.isValid&&(this._config=e.detail.value,this._errors=void 0,this._dirty=!0)}},{kind:"field",key:"_backTapped",value(){return()=>{this._dirty?(0,u.g7)(this,{text:this.hass.localize("ui.panel.config.common.editor.confirm_unsaved"),confirmText:this.hass.localize("ui.common.leave"),dismissText:this.hass.localize("ui.common.stay"),confirm:()=>{setTimeout((()=>history.back()))}}):history.back()}}},{kind:"method",key:"_duplicate",value:async function(){var e;if(this._dirty){if(!await(0,u.g7)(this,{text:this.hass.localize("ui.panel.config.common.editor.confirm_unsaved"),confirmText:this.hass.localize("ui.common.yes"),dismissText:this.hass.localize("ui.common.no")}))return;await new Promise((e=>setTimeout(e,0)))}(0,h.rg)({...this._config,alias:`${null===(e=this._config)||void 0===e?void 0:e.alias} (${this.hass.localize("ui.panel.config.script.picker.duplicate")})`})}},{kind:"method",key:"_deleteConfirm",value:async function(){(0,u.g7)(this,{text:this.hass.localize("ui.panel.config.script.editor.delete_confirm"),confirmText:this.hass.localize("ui.common.delete"),dismissText:this.hass.localize("ui.common.cancel"),confirm:()=>this._delete()})}},{kind:"method",key:"_delete",value:async function(){await(0,h.oR)(this.hass,(0,s.p)(this.scriptEntityId)),history.back()}},{kind:"method",key:"_handleMenuAction",value:async function(e){switch(e.detail.index){case 0:this._mode="gui";break;case 1:this._mode="yaml";break;case 2:this._duplicate();break;case 3:this._deleteConfirm()}}},{kind:"method",key:"_saveScript",value:function(){if(this._idError)return void(0,y.C)(this,{message:this.hass.localize("ui.panel.config.script.editor.id_already_exists_save_error"),dismissable:!1,duration:0,action:{action:()=>{},text:this.hass.localize("ui.dialogs.generic.ok")}});const e=this.scriptEntityId?(0,s.p)(this.scriptEntityId):this._entityId||Date.now();this.hass.callApi("POST","config/script/config/"+e,this._config).then((()=>{this._dirty=!1,this.scriptEntityId||(0,a.c)(`/config/script/edit/${e}`,{replace:!0})}),(e=>{throw this._errors=e.body.message||e.error||e.body,(0,y.C)(this,{message:e.body.message||e.error||e.body}),e}))}},{kind:"method",key:"handleKeyboardSave",value:function(){this._saveScript()}},{kind:"get",static:!0,key:"styles",value:function(){return[f.Qx,t.iv`
        ha-card {
          overflow: hidden;
        }
        p {
          margin-bottom: 0;
        }
        .errors {
          padding: 20px;
          font-weight: bold;
          color: var(--error-color);
        }
        .content {
          padding: 16px 16px 20px;
        }
        .yaml-mode {
          height: 100%;
          display: flex;
          flex-direction: column;
          padding-bottom: 0;
        }
        ha-yaml-editor {
          flex-grow: 1;
          --code-mirror-height: 100%;
          min-height: 0;
        }
        .yaml-mode ha-card {
          overflow: initial;
          --ha-card-border-radius: 0;
          border-bottom: 1px solid var(--divider-color);
        }
        span[slot="introduction"] a {
          color: var(--primary-color);
        }
        ha-fab {
          position: relative;
          bottom: calc(-80px - env(safe-area-inset-bottom));
          transition: bottom 0.3s;
        }
        ha-fab.dirty {
          bottom: 0;
        }
        .selected_menu_item {
          color: var(--primary-color);
        }
        li[role="separator"] {
          border-bottom-color: var(--divider-color);
        }
        .header {
          display: flex;
          margin: 16px 0;
          align-items: center;
        }
        .header .name {
          font-size: 20px;
          font-weight: 400;
          flex: 1;
        }
        .header a {
          color: var(--secondary-text-color);
        }
      `]}}]}}),(0,p.U)(t.oi));customElements.define("ha-script-editor",D)}))},25931:(e,t,i)=>{i.a(e,(async e=>{var t=i(37500),r=i(33310),n=i(14516),o=i(44583),s=i(47181),a=i(27269),l=i(91741),c=i(83849),d=i(87744),h=(i(67556),i(36125),i(10983),i(48429),i(52039),i(44547)),u=i(26765),p=(i(96551),i(11654)),f=i(27322),m=i(81796),y=i(29311),v=e([o]);function g(){g=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!w(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return C(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?C(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=$(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:E(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=E(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function b(e){var t,i=$(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function k(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function w(e){return e.decorators&&e.decorators.length}function _(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function E(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function $(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function C(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}o=(v.then?await v:v)[0];!function(e,t,i,r){var n=g();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),i),a=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(_(o.descriptor)||_(n.descriptor)){if(w(o)||w(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(w(o)){if(w(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}k(o,n)}else t.push(o)}return t}(s.d.map(b)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,r.Mo)("ha-script-picker")],(function(e,i){return{F:class extends i{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,r.Cb)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"scripts",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"isWide",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"narrow",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"route",value:void 0},{kind:"field",decorators:[(0,r.Cb)()],key:"_activeFilters",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_filteredScripts",value:void 0},{kind:"field",decorators:[(0,r.SB)()],key:"_filterValue",value:void 0},{kind:"field",key:"_scripts",value:()=>(0,n.Z)(((e,t)=>null===t?[]:(t?e.filter((e=>t.includes(e.entity_id))):e).map((e=>({...e,name:(0,l.C)(e),last_triggered:e.attributes.last_triggered||void 0})))))},{kind:"field",key:"_columns",value(){return(0,n.Z)(((e,i)=>{const r={icon:{title:"",label:this.hass.localize("ui.panel.config.script.picker.headers.state"),type:"icon",template:(e,i)=>t.dy` <ha-state-icon .state=${i}></ha-state-icon>`},name:{title:this.hass.localize("ui.panel.config.script.picker.headers.name"),sortable:!0,filterable:!0,direction:"asc",grows:!0,template:e?(e,i)=>t.dy`
              ${e}
              <div class="secondary">
                ${this.hass.localize("ui.card.automation.last_triggered")}:
                ${i.attributes.last_triggered?(0,o.o0)(new Date(i.attributes.last_triggered),this.hass.locale):this.hass.localize("ui.components.relative_time.never")}
              </div>
            `:void 0}};return e||(r.last_triggered={sortable:!0,width:"40%",title:this.hass.localize("ui.card.automation.last_triggered"),template:e=>t.dy`
          ${e?(0,o.o0)(new Date(e),this.hass.locale):this.hass.localize("ui.components.relative_time.never")}
        `}),r.actions={title:"",width:this.narrow?void 0:"10%",type:"overflow-menu",template:(e,i)=>t.dy`
          <ha-icon-overflow-menu
            .hass=${this.hass}
            narrow
            .items=${[{path:"M11,9H13V7H11M12,20C7.59,20 4,16.41 4,12C4,7.59 7.59,4 12,4C16.41,4 20,7.59 20,12C20,16.41 16.41,20 12,20M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M11,17H13V11H11V17Z",label:this.hass.localize("ui.panel.config.script.picker.show_info"),action:()=>this._showInfo(i)},{path:"M8,5.14V19.14L19,12.14L8,5.14Z",label:this.hass.localize("ui.panel.config.script.picker.run"),action:()=>this._runScript(i)},{path:"M15,12C15,10.7 14.16,9.6 13,9.18V6.82C14.16,6.4 15,5.3 15,4A3,3 0 0,0 12,1A3,3 0 0,0 9,4C9,5.3 9.84,6.4 11,6.82V9.19C9.84,9.6 9,10.7 9,12C9,13.3 9.84,14.4 11,14.82V17.18C9.84,17.6 9,18.7 9,20A3,3 0 0,0 12,23A3,3 0 0,0 15,20C15,18.7 14.16,17.6 13,17.18V14.82C14.16,14.4 15,13.3 15,12M12,3A1,1 0 0,1 13,4A1,1 0 0,1 12,5A1,1 0 0,1 11,4A1,1 0 0,1 12,3M12,21A1,1 0 0,1 11,20A1,1 0 0,1 12,19A1,1 0 0,1 13,20A1,1 0 0,1 12,21Z",label:this.hass.localize("ui.panel.config.script.picker.show_trace"),action:()=>this._showTrace(i)},{path:"M11,17H4A2,2 0 0,1 2,15V3A2,2 0 0,1 4,1H16V3H4V15H11V13L15,16L11,19V17M19,21V7H8V13H6V7A2,2 0 0,1 8,5H19A2,2 0 0,1 21,7V21A2,2 0 0,1 19,23H8A2,2 0 0,1 6,21V19H8V21H19Z",label:this.hass.localize("ui.panel.config.script.picker.duplicate"),action:()=>this._duplicate(i)},{label:this.hass.localize("ui.panel.config.script.picker.delete"),path:"M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z",action:()=>this._deleteConfirm(i),warning:!0}]}
          >
          </ha-icon-overflow-menu>
        `},r}))}},{kind:"method",key:"render",value:function(){return t.dy`
      <hass-tabs-subpage-data-table
        .hass=${this.hass}
        .narrow=${this.narrow}
        back-path="/config"
        .route=${this.route}
        .tabs=${y.configSections.automations}
        .columns=${this._columns(this.narrow,this.hass.locale)}
        .data=${this._scripts(this.scripts,this._filteredScripts)}
        .activeFilters=${this._activeFilters}
        id="entity_id"
        .noDataText=${this.hass.localize("ui.panel.config.script.picker.no_scripts")}
        @clear-filter=${this._clearFilter}
        hasFab
        clickable
        @row-click=${this._handleRowClicked}
      >
        <ha-icon-button
          slot="toolbar-icon"
          .label=${this.hass.localize("ui.common.help")}
          .path=${"M15.07,11.25L14.17,12.17C13.45,12.89 13,13.5 13,15H11V14.5C11,13.39 11.45,12.39 12.17,11.67L13.41,10.41C13.78,10.05 14,9.55 14,9C14,7.89 13.1,7 12,7A2,2 0 0,0 10,9H8A4,4 0 0,1 12,5A4,4 0 0,1 16,9C16,9.88 15.64,10.67 15.07,11.25M13,19H11V17H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12C22,6.47 17.5,2 12,2Z"}
          @click=${this._showHelp}
        ></ha-icon-button>
        <ha-button-related-filter-menu
          slot="filter-menu"
          corner="BOTTOM_START"
          .narrow=${this.narrow}
          .hass=${this.hass}
          .value=${this._filterValue}
          exclude-domains='["script"]'
          @related-changed=${this._relatedFilterChanged}
        >
        </ha-button-related-filter-menu>
        <a href="/config/script/edit/new" slot="fab">
          <ha-fab
            ?is-wide=${this.isWide}
            ?narrow=${this.narrow}
            .label=${this.hass.localize("ui.panel.config.script.picker.add_script")}
            extended
            ?rtl=${(0,d.HE)(this.hass)}
          >
            <ha-svg-icon slot="icon" .path=${"M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z"}></ha-svg-icon>
          </ha-fab>
        </a>
      </hass-tabs-subpage-data-table>
    `}},{kind:"method",key:"_relatedFilterChanged",value:function(e){this._filterValue=e.detail.value,this._filterValue?(this._activeFilters=[e.detail.filter],this._filteredScripts=e.detail.items.script||null):this._clearFilter()}},{kind:"method",key:"_clearFilter",value:function(){this._filteredScripts=void 0,this._activeFilters=void 0,this._filterValue=void 0}},{kind:"method",key:"_handleRowClicked",value:function(e){(0,c.c)(`/config/script/edit/${e.detail.id}`)}},{kind:"field",key:"_runScript",value(){return async e=>{await(0,h.kC)(this.hass,e.entity_id),(0,m.C)(this,{message:this.hass.localize("ui.notification_toast.triggered","name",(0,l.C)(e))})}}},{kind:"method",key:"_showInfo",value:function(e){(0,s.B)(this,"hass-more-info",{entityId:e.entity_id})}},{kind:"method",key:"_showTrace",value:function(e){(0,c.c)(`/config/script/trace/${e.entity_id}`)}},{kind:"method",key:"_showHelp",value:function(){(0,u.Ys)(this,{title:this.hass.localize("ui.panel.config.script.caption"),text:t.dy`
        ${this.hass.localize("ui.panel.config.script.picker.introduction")}
        <p>
          <a
            href=${(0,f.R)(this.hass,"/docs/scripts/")}
            target="_blank"
            rel="noreferrer"
          >
            ${this.hass.localize("ui.panel.config.script.picker.learn_more")}
          </a>
        </p>
      `})}},{kind:"method",key:"_duplicate",value:async function(e){const t=await(0,h.Vn)(this.hass,(0,a.p)(e.entity_id));(0,h.rg)({...t,alias:`${null==t?void 0:t.alias} (${this.hass.localize("ui.panel.config.script.picker.duplicate")})`})}},{kind:"method",key:"_deleteConfirm",value:async function(e){(0,u.g7)(this,{text:this.hass.localize("ui.panel.config.script.editor.delete_confirm"),confirmText:this.hass.localize("ui.common.delete"),dismissText:this.hass.localize("ui.common.cancel"),confirm:()=>this._delete(e)})}},{kind:"method",key:"_delete",value:async function(e){await(0,h.oR)(this.hass,(0,a.p)(e.entity_id))}},{kind:"get",static:!0,key:"styles",value:function(){return[p.Qx,t.iv`
        a {
          text-decoration: none;
        }
      `]}}]}}),t.oi)}))}}]);
//# sourceMappingURL=a264a604.js.map