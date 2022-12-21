// browsified from https://github.com/ssleptsov/ninja-keys

(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    exports.baseStyles = void 0;
    var _lit = require("lit");
    const baseStyles = (0, _lit.css)`
      :host {
        --ninja-width: 640px;
        --ninja-backdrop-filter: none;
        --ninja-overflow-background: rgba(255, 255, 255, 0.5);
        --ninja-text-color: rgb(60, 65, 73);
        --ninja-font-size: 16px;
        --ninja-top: 20%;
    
        --ninja-key-border-radius: 0.25em;
        --ninja-accent-color: rgb(110, 94, 210);
        --ninja-secondary-background-color: rgb(239, 241, 244);
        --ninja-secondary-text-color: rgb(107, 111, 118);
    
        --ninja-selected-background: rgb(248, 249, 251);
    
        --ninja-icon-color: var(--ninja-secondary-text-color);
        --ninja-icon-size: 1.2em;
        --ninja-separate-border: 1px solid var(--ninja-secondary-background-color);
    
        --ninja-modal-background: #fff;
        --ninja-modal-shadow: rgb(0 0 0 / 50%) 0px 16px 70px;
    
        --ninja-actions-height: 300px;
        --ninja-group-text-color: rgb(144, 149, 157);
    
        --ninja-footer-background: rgba(242, 242, 242, 0.4);
    
        --ninja-placeholder-color: #8e8e8e;
    
        font-size: var(--ninja-font-size);
    
        --ninja-z-index: 1;
      }
    
      :host(.dark) {
        --ninja-backdrop-filter: none;
        --ninja-overflow-background: rgba(0, 0, 0, 0.7);
        --ninja-text-color: #7d7d7d;
    
        --ninja-modal-background: rgba(17, 17, 17, 0.85);
        --ninja-accent-color: rgb(110, 94, 210);
        --ninja-secondary-background-color: rgba(51, 51, 51, 0.44);
        --ninja-secondary-text-color: #888;
    
        --ninja-selected-text-color: #eaeaea;
        --ninja-selected-background: rgba(51, 51, 51, 0.44);
    
        --ninja-icon-color: var(--ninja-secondary-text-color);
        --ninja-separate-border: 1px solid var(--ninja-secondary-background-color);
    
        --ninja-modal-shadow: 0 16px 70px rgba(0, 0, 0, 0.2);
    
        --ninja-group-text-color: rgb(144, 149, 157);
    
        --ninja-footer-background: rgba(30, 30, 30, 85%);
      }
    
      .modal {
        display: none;
        position: fixed;
        z-index: var(--ninja-z-index);
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        overflow: auto;
        background: var(--ninja-overflow-background);
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        -webkit-backdrop-filter: var(--ninja-backdrop-filter);
        backdrop-filter: var(--ninja-backdrop-filter);
        text-align: left;
        color: var(--ninja-text-color);
        font-family: var(--ninja-font-family);
      }
      .modal.visible {
        display: block;
      }
    
      .modal-content {
        position: relative;
        top: var(--ninja-top);
        margin: auto;
        padding: 0;
        display: flex;
        flex-direction: column;
        flex-shrink: 1;
        -webkit-box-flex: 1;
        flex-grow: 1;
        min-width: 0px;
        will-change: transform;
        background: var(--ninja-modal-background);
        border-radius: 0.5em;
        box-shadow: var(--ninja-modal-shadow);
        max-width: var(--ninja-width);
        overflow: hidden;
      }
    
      .bump {
        animation: zoom-in-zoom-out 0.2s ease;
      }
    
      @keyframes zoom-in-zoom-out {
        0% {
          transform: scale(0.99);
        }
        50% {
          transform: scale(1.01, 1.01);
        }
        100% {
          transform: scale(1, 1);
        }
      }
    
      .ninja-github {
        color: var(--ninja-keys-text-color);
        font-weight: normal;
        text-decoration: none;
      }
    
      .actions-list {
        max-height: var(--ninja-actions-height);
        overflow: auto;
        scroll-behavior: smooth;
        position: relative;
        margin: 0;
        padding: 0.5em 0;
        list-style: none;
        scroll-behavior: smooth;
      }
    
      .group-header {
        height: 1.375em;
        line-height: 1.375em;
        padding-left: 1.25em;
        padding-top: 0.5em;
        text-overflow: ellipsis;
        white-space: nowrap;
        overflow: hidden;
        font-size: 0.75em;
        line-height: 1em;
        color: var(--ninja-group-text-color);
        margin: 1px 0;
      }
    
      .modal-footer {
        background: var(--ninja-footer-background);
        padding: 0.5em 1em;
        display: flex;
        /* font-size: 0.75em; */
        border-top: var(--ninja-separate-border);
        color: var(--ninja-secondary-text-color);
      }
    
      .modal-footer .help {
        display: flex;
        margin-right: 1em;
        align-items: center;
        font-size: 0.75em;
      }
    
      .ninja-examplekey {
        background: var(--ninja-secondary-background-color);
        padding: 0.06em 0.25em;
        border-radius: var(--ninja-key-border-radius);
        color: var(--ninja-secondary-text-color);
        width: 1em;
        height: 1em;
        margin-right: 0.5em;
        font-size: 1.25em;
        fill: currentColor;
      }
      .ninja-examplekey.esc {
        width: auto;
        height: auto;
        font-size: 1.1em;
      }
      .ninja-examplekey.backspace {
        opacity: 0.7;
      }
    `;
    exports.baseStyles = baseStyles;
    
    },{"lit":39}],2:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    exports.NinjaAction = void 0;
    var _lit = require("lit");
    var _decorators = require("lit/decorators.js");
    var _classMap = require("lit/directives/class-map.js");
    var _unsafeHtml = require("lit/directives/unsafe-html.js");
    var _join = require("lit/directives/join.js");
    require("@material/mwc-icon");
    var __decorate = void 0 && (void 0).__decorate || function (decorators, target, key, desc) {
      var c = arguments.length,
        r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc,
        d;
      if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
      return c > 3 && r && Object.defineProperty(target, key, r), r;
    };
    let NinjaAction = class NinjaAction extends _lit.LitElement {
      constructor() {
        super();
        this.selected = false;
        /**
         * Display hotkey as separate buttons on UI or as is
         */
        this.hotKeysJoinedView = true;
        this.addEventListener('click', this.click);
      }
      /**
       * Scroll to show element
       */
      ensureInView() {
        requestAnimationFrame(() => this.scrollIntoView({
          block: 'nearest'
        }));
      }
      click() {
        this.dispatchEvent(new CustomEvent('actionsSelected', {
          detail: this.action,
          bubbles: true,
          composed: true
        }));
      }
      updated(changedProperties) {
        if (changedProperties.has('selected')) {
          if (this.selected) {
            this.ensureInView();
          }
        }
      }
      render() {
        let icon;
        if (this.action.mdIcon) {
          icon = (0, _lit.html)`<mwc-icon part="ninja-icon" class="ninja-icon"
            >${this.action.mdIcon}</mwc-icon
          >`;
        } else if (this.action.icon) {
          icon = (0, _unsafeHtml.unsafeHTML)(this.action.icon || '');
        }
        // const hotkey = this.action.hotkey
        //   ? html`<div class="ninja-hotkey">${this.action.hotkey}</div>`
        //   : '';
        let hotkey;
        if (this.action.hotkey) {
          if (this.hotKeysJoinedView) {
            hotkey = this.action.hotkey.split(',').map(hotkeys => {
              const keys = hotkeys.split('+');
              const joinedKeys = (0, _lit.html)`${(0, _join.join)(keys.map(key => (0, _lit.html)`<kbd>${key}</kbd>`), '+')}`;
              return (0, _lit.html)`<div class="ninja-hotkey ninja-hotkeys">
                ${joinedKeys}
              </div>`;
            });
          } else {
            hotkey = this.action.hotkey.split(',').map(hotkeys => {
              const keys = hotkeys.split('+');
              const keyElements = keys.map(key => (0, _lit.html)`<kbd class="ninja-hotkey">${key}</kbd>`);
              return (0, _lit.html)`<kbd class="ninja-hotkeys">${keyElements}</kbd>`;
            });
          }
        }
        const classes = {
          selected: this.selected,
          'ninja-action': true
        };
        return (0, _lit.html)`
          <div
            class="ninja-action"
            part="ninja-action ${this.selected ? 'ninja-selected' : ''}"
            class=${(0, _classMap.classMap)(classes)}
          >
            ${icon}
            <div class="ninja-title">${this.action.title}</div>
            ${hotkey}
          </div>
        `;
      }
    };
    exports.NinjaAction = NinjaAction;
    NinjaAction.styles = (0, _lit.css)`
        :host {
          display: flex;
          width: 100%;
        }
        .ninja-action {
          padding: 0.75em 1em;
          display: flex;
          border-left: 2px solid transparent;
          align-items: center;
          justify-content: start;
          outline: none;
          transition: color 0s ease 0s;
          width: 100%;
        }
        .ninja-action.selected {
          cursor: pointer;
          color: var(--ninja-selected-text-color);
          background-color: var(--ninja-selected-background);
          border-left: 2px solid var(--ninja-accent-color);
          outline: none;
        }
        .ninja-action.selected .ninja-icon {
          color: var(--ninja-selected-text-color);
        }
        .ninja-icon {
          font-size: var(--ninja-icon-size);
          max-width: var(--ninja-icon-size);
          max-height: var(--ninja-icon-size);
          margin-right: 1em;
          color: var(--ninja-icon-color);
          margin-right: 1em;
          position: relative;
        }
    
        .ninja-title {
          flex-shrink: 0.01;
          margin-right: 0.5em;
          flex-grow: 1;
          font-size: 0.8125em;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }
        .ninja-hotkeys {
          flex-shrink: 0;
          width: min-content;
          display: flex;
        }
    
        .ninja-hotkeys kbd {
          font-family: inherit;
        }
        .ninja-hotkey {
          background: var(--ninja-secondary-background-color);
          padding: 0.06em 0.25em;
          border-radius: var(--ninja-key-border-radius);
          text-transform: capitalize;
          color: var(--ninja-secondary-text-color);
          font-size: 0.75em;
          font-family: inherit;
        }
    
        .ninja-hotkey + .ninja-hotkey {
          margin-left: 0.5em;
        }
        .ninja-hotkeys + .ninja-hotkeys {
          margin-left: 1em;
        }
      `;
    __decorate([(0, _decorators.property)({
      type: Object
    })], NinjaAction.prototype, "action", void 0);
    __decorate([(0, _decorators.property)({
      type: Boolean
    })], NinjaAction.prototype, "selected", void 0);
    __decorate([(0, _decorators.property)({
      type: Boolean
    })], NinjaAction.prototype, "hotKeysJoinedView", void 0);
    exports.NinjaAction = NinjaAction = __decorate([(0, _decorators.customElement)('ninja-action')], NinjaAction);
    
    },{"@material/mwc-icon":19,"lit":39,"lit/decorators.js":32,"lit/directives/class-map.js":33,"lit/directives/join.js":34,"lit/directives/unsafe-html.js":38}],3:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    exports.footerHtml = void 0;
    var _lit = require("lit");
    const footerHtml = (0, _lit.html)` <div class="modal-footer" slot="footer">
      <span class="help">
        <svg
          version="1.0"
          class="ninja-examplekey"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 1280 1280"
        >
          <path
            d="M1013 376c0 73.4-.4 113.3-1.1 120.2a159.9 159.9 0 0 1-90.2 127.3c-20 9.6-36.7 14-59.2 15.5-7.1.5-121.9.9-255 1h-242l95.5-95.5 95.5-95.5-38.3-38.2-38.2-38.3-160 160c-88 88-160 160.4-160 161 0 .6 72 73 160 161l160 160 38.2-38.3 38.3-38.2-95.5-95.5-95.5-95.5h251.1c252.9 0 259.8-.1 281.4-3.6 72.1-11.8 136.9-54.1 178.5-116.4 8.6-12.9 22.6-40.5 28-55.4 4.4-12 10.7-36.1 13.1-50.6 1.6-9.6 1.8-21 2.1-132.8l.4-122.2H1013v110z"
          />
        </svg>
    
        to select
      </span>
      <span class="help">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="ninja-examplekey"
          viewBox="0 0 24 24"
        >
          <path d="M0 0h24v24H0V0z" fill="none" />
          <path
            d="M20 12l-1.41-1.41L13 16.17V4h-2v12.17l-5.58-5.59L4 12l8 8 8-8z"
          />
        </svg>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="ninja-examplekey"
          viewBox="0 0 24 24"
        >
          <path d="M0 0h24v24H0V0z" fill="none" />
          <path d="M4 12l1.41 1.41L11 7.83V20h2V7.83l5.58 5.59L20 12l-8-8-8 8z" />
        </svg>
        to navigate
      </span>
      <span class="help">
        <span class="ninja-examplekey esc">esc</span>
        to close
      </span>
      <span class="help">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="ninja-examplekey backspace"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fill-rule="evenodd"
            d="M6.707 4.879A3 3 0 018.828 4H15a3 3 0 013 3v6a3 3 0 01-3 3H8.828a3 3 0 01-2.12-.879l-4.415-4.414a1 1 0 010-1.414l4.414-4.414zm4 2.414a1 1 0 00-1.414 1.414L10.586 10l-1.293 1.293a1 1 0 101.414 1.414L12 11.414l1.293 1.293a1 1 0 001.414-1.414L13.414 10l1.293-1.293a1 1 0 00-1.414-1.414L12 8.586l-1.293-1.293z"
            clip-rule="evenodd"
          />
        </svg>
        move to parent
      </span>
    </div>`;
    exports.footerHtml = footerHtml;
    
    },{"lit":39}],4:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    exports.NinjaHeader = void 0;
    var _lit = require("lit");
    var _decorators = require("lit/decorators.js");
    var _ref = require("lit/directives/ref.js");
    var __decorate = void 0 && (void 0).__decorate || function (decorators, target, key, desc) {
      var c = arguments.length,
        r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc,
        d;
      if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
      return c > 3 && r && Object.defineProperty(target, key, r), r;
    };
    let NinjaHeader = class NinjaHeader extends _lit.LitElement {
      constructor() {
        super(...arguments);
        this.placeholder = '';
        this.hideBreadcrumbs = false;
        this.breadcrumbHome = 'Home';
        this.breadcrumbs = [];
        this._inputRef = (0, _ref.createRef)();
      }
      render() {
        let breadcrumbs = '';
        if (!this.hideBreadcrumbs) {
          const itemTemplates = [];
          for (const breadcrumb of this.breadcrumbs) {
            itemTemplates.push((0, _lit.html)`<button
                tabindex="-1"
                @click=${() => this.selectParent(breadcrumb)}
                class="breadcrumb"
              >
                ${breadcrumb}
              </button>`);
          }
          breadcrumbs = (0, _lit.html)`<div class="breadcrumb-list">
            <button
              tabindex="-1"
              @click=${() => this.selectParent()}
              class="breadcrumb"
            >
              ${this.breadcrumbHome}
            </button>
            ${itemTemplates}
          </div>`;
        }
        return (0, _lit.html)`
          ${breadcrumbs}
          <div part="ninja-input-wrapper" class="search-wrapper">
            <input
              part="ninja-input"
              type="text"
              id="search"
              spellcheck="false"
              autocomplete="off"
              @input="${this._handleInput}"
              ${(0, _ref.ref)(this._inputRef)}
              placeholder="${this.placeholder}"
              class="search"
            />
          </div>
        `;
      }
      setSearch(value) {
        if (this._inputRef.value) {
          this._inputRef.value.value = value;
        }
      }
      focusSearch() {
        requestAnimationFrame(() => this._inputRef.value.focus());
      }
      _handleInput(event) {
        const input = event.target;
        this.dispatchEvent(new CustomEvent('change', {
          detail: {
            search: input.value
          },
          bubbles: false,
          composed: false
        }));
      }
      selectParent(breadcrumb) {
        this.dispatchEvent(new CustomEvent('setParent', {
          detail: {
            parent: breadcrumb
          },
          bubbles: true,
          composed: true
        }));
      }
      firstUpdated() {
        this.focusSearch();
      }
      _close() {
        this.dispatchEvent(new CustomEvent('close', {
          bubbles: true,
          composed: true
        }));
      }
    };
    exports.NinjaHeader = NinjaHeader;
    NinjaHeader.styles = (0, _lit.css)`
        :host {
          flex: 1;
          position: relative;
        }
        .search {
          padding: 1.25em;
          flex-grow: 1;
          flex-shrink: 0;
          margin: 0px;
          border: none;
          appearance: none;
          font-size: 1.125em;
          background: transparent;
          caret-color: var(--ninja-accent-color);
          color: var(--ninja-text-color);
          outline: none;
          font-family: var(--ninja-font-family);
        }
        .search::placeholder {
          color: var(--ninja-placeholder-color);
        }
        .breadcrumb-list {
          padding: 1em 4em 0 1em;
          display: flex;
          flex-direction: row;
          align-items: stretch;
          justify-content: flex-start;
          flex: initial;
        }
    
        .breadcrumb {
          background: var(--ninja-secondary-background-color);
          text-align: center;
          line-height: 1.2em;
          border-radius: var(--ninja-key-border-radius);
          border: 0;
          cursor: pointer;
          padding: 0.1em 0.5em;
          color: var(--ninja-secondary-text-color);
          margin-right: 0.5em;
          outline: none;
          font-family: var(--ninja-font-family);
        }
    
        .search-wrapper {
          display: flex;
          border-bottom: var(--ninja-separate-border);
        }
      `;
    __decorate([(0, _decorators.property)()], NinjaHeader.prototype, "placeholder", void 0);
    __decorate([(0, _decorators.property)({
      type: Boolean
    })], NinjaHeader.prototype, "hideBreadcrumbs", void 0);
    __decorate([(0, _decorators.property)()], NinjaHeader.prototype, "breadcrumbHome", void 0);
    __decorate([(0, _decorators.property)({
      type: Array
    })], NinjaHeader.prototype, "breadcrumbs", void 0);
    exports.NinjaHeader = NinjaHeader = __decorate([(0, _decorators.customElement)('ninja-header')], NinjaHeader);
    
    },{"lit":39,"lit/decorators.js":32,"lit/directives/ref.js":36}],5:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    exports.NinjaKeys = void 0;
    var _lit = require("lit");
    var _decorators = require("lit/decorators.js");
    var _repeat = require("lit/directives/repeat.js");
    var _live = require("lit/directives/live.js");
    var _ref = require("lit-html/directives/ref.js");
    var _classMap = require("lit/directives/class-map.js");
    var _hotkeysJs = _interopRequireDefault(require("hotkeys-js"));
    require("./ninja-header.js");
    require("./ninja-action.js");
    var _ninjaFooter = require("./ninja-footer.js");
    var _baseStyles = require("./base-styles.js");
    function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
    var __decorate = void 0 && (void 0).__decorate || function (decorators, target, key, desc) {
      var c = arguments.length,
        r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc,
        d;
      if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
      return c > 3 && r && Object.defineProperty(target, key, r), r;
    };
    let NinjaKeys = class NinjaKeys extends _lit.LitElement {
      constructor() {
        super(...arguments);
        /**
         * Search placeholder text
         */
        this.placeholder = 'Type a command or search...';
        /**
         * If true will register all hotkey for all actions
         */
        this.disableHotkeys = false;
        /**
         * Show or hide breadcrumbs on header
         */
        this.hideBreadcrumbs = false;
        /**
         * Open or hide shorcut
         */
        this.openHotkey = 'cmd+k,ctrl+k';
        /**
         * Navigation Up hotkey
         */
        this.navigationUpHotkey = 'up,shift+tab';
        /**
         * Navigation Down hotkey
         */
        this.navigationDownHotkey = 'down,tab';
        /**
         * Close hotkey
         */
        this.closeHotkey = 'esc';
        /**
         * Go back on one level if has parent menu
         */
        this.goBackHotkey = 'backspace';
        /**
         * Select action and execute handler or open submenu
         */
        this.selectHotkey = 'enter'; // enter,space
        /**
         * Show or hide breadcrumbs on header
         */
        this.hotKeysJoinedView = false;
        /**
         * Disable load material icons font on connect
         * If you use custom icons.
         * Set this attribute to prevent load default icons font
         */
        this.noAutoLoadMdIcons = false;
        /**
         * Array of actions
         */
        this.data = [];
        /**
         * Show or hide element
         */
        this.visible = false;
        /**
         * Temproray used for animation effect. TODO: change to animate logic
         */
        this._bump = true;
        this._actionMatches = [];
        this._search = '';
        /**
         * Array of actions in flat structure
         */
        this._flatData = [];
        this._headerRef = (0, _ref.createRef)();
      }
      /**
       * Public methods
       */
      /**
       * Show a modal
       */
      open(options = {}) {
        this._bump = true;
        this.visible = true;
        this._headerRef.value.focusSearch();
        if (this._actionMatches.length > 0) {
          this._selected = this._actionMatches[0];
        }
        this.setParent(options.parent);
      }
      /**
       * Close modal
       */
      close() {
        this._bump = false;
        this.visible = false;
      }
      /**
       * Navigate to group of actions
       * @param parent id of parent group/action
       */
      setParent(parent) {
        if (!parent) {
          this._currentRoot = undefined;
          // this.breadcrumbs = [];
        } else {
          this._currentRoot = parent;
        }
        this._selected = undefined;
        this._search = '';
        this._headerRef.value.setSearch('');
      }
      get breadcrumbs() {
        var _a;
        const path = [];
        let parentAction = (_a = this._selected) === null || _a === void 0 ? void 0 : _a.parent;
        if (parentAction) {
          path.push(parentAction);
          while (parentAction) {
            const action = this._flatData.find(a => a.id === parentAction);
            if (action === null || action === void 0 ? void 0 : action.parent) {
              path.push(action.parent);
            }
            parentAction = action ? action.parent : undefined;
          }
        }
        return path.reverse();
      }
      connectedCallback() {
        super.connectedCallback();
        if (!this.noAutoLoadMdIcons) {
          document.fonts.load('24px Material Icons', 'apps').then(() => {});
        }
        this._registerInternalHotkeys();
      }
      disconnectedCallback() {
        super.disconnectedCallback();
        this._unregisterInternalHotkeys();
      }
      _flattern(members, parent) {
        let children = [];
        if (!members) {
          members = [];
        }
        return members.map(mem => {
          const alreadyFlatternByUser = mem.children && mem.children.some(value => {
            return typeof value == 'string';
          });
          const m = {
            ...mem,
            parent: mem.parent || parent
          };
          if (alreadyFlatternByUser) {
            return m;
          } else {
            if (m.children && m.children.length) {
              parent = mem.id;
              children = [...children, ...m.children];
            }
            m.children = m.children ? m.children.map(c => c.id) : [];
            return m;
          }
        }).concat(children.length ? this._flattern(children, parent) : children);
      }
      update(changedProperties) {
        if (changedProperties.has('data') && !this.disableHotkeys) {
          this._flatData = this._flattern(this.data);
          this._flatData.filter(action => !!action.hotkey).forEach(action => {
            (0, _hotkeysJs.default)(action.hotkey, event => {
              event.preventDefault();
              if (action.handler) {
                action.handler(action);
              }
            });
          });
        }
        super.update(changedProperties);
      }
      _registerInternalHotkeys() {
        if (this.openHotkey) {
          (0, _hotkeysJs.default)(this.openHotkey, event => {
            event.preventDefault();
            this.visible ? this.close() : this.open();
          });
        }
        if (this.selectHotkey) {
          (0, _hotkeysJs.default)(this.selectHotkey, event => {
            if (!this.visible) {
              return;
            }
            event.preventDefault();
            this._actionSelected(this._actionMatches[this._selectedIndex]);
          });
        }
        if (this.goBackHotkey) {
          (0, _hotkeysJs.default)(this.goBackHotkey, event => {
            if (!this.visible) {
              return;
            }
            if (!this._search) {
              event.preventDefault();
              this._goBack();
            }
          });
        }
        if (this.navigationDownHotkey) {
          (0, _hotkeysJs.default)(this.navigationDownHotkey, event => {
            if (!this.visible) {
              return;
            }
            event.preventDefault();
            if (this._selectedIndex >= this._actionMatches.length - 1) {
              this._selected = this._actionMatches[0];
            } else {
              this._selected = this._actionMatches[this._selectedIndex + 1];
            }
          });
        }
        if (this.navigationUpHotkey) {
          (0, _hotkeysJs.default)(this.navigationUpHotkey, event => {
            if (!this.visible) {
              return;
            }
            event.preventDefault();
            if (this._selectedIndex === 0) {
              this._selected = this._actionMatches[this._actionMatches.length - 1];
            } else {
              this._selected = this._actionMatches[this._selectedIndex - 1];
            }
          });
        }
        if (this.closeHotkey) {
          (0, _hotkeysJs.default)(this.closeHotkey, () => {
            if (!this.visible) {
              return;
            }
            this.close();
          });
        }
      }
      _unregisterInternalHotkeys() {
        if (this.openHotkey) {
          _hotkeysJs.default.unbind(this.openHotkey);
        }
        if (this.selectHotkey) {
          _hotkeysJs.default.unbind(this.selectHotkey);
        }
        if (this.goBackHotkey) {
          _hotkeysJs.default.unbind(this.goBackHotkey);
        }
        if (this.navigationDownHotkey) {
          _hotkeysJs.default.unbind(this.navigationDownHotkey);
        }
        if (this.navigationUpHotkey) {
          _hotkeysJs.default.unbind(this.navigationUpHotkey);
        }
        if (this.closeHotkey) {
          _hotkeysJs.default.unbind(this.closeHotkey);
        }
      }
      _actionFocused(index, $event) {
        // this.selectedIndex = index;
        this._selected = index;
        $event.target.ensureInView();
      }
      _onTransitionEnd() {
        this._bump = false;
      }
      _goBack() {
        const parent = this.breadcrumbs.length > 1 ? this.breadcrumbs[this.breadcrumbs.length - 2] : undefined;
        this.setParent(parent);
      }
      render() {
        const classes = {
          bump: this._bump,
          'modal-content': true
        };
        const menuClasses = {
          visible: this.visible,
          modal: true
        };
        const actionMatches = this._flatData.filter(action => {
          var _a;
          const regex = new RegExp(this._search, 'gi');
          const matcher = action.title.match(regex) || ((_a = action.keywords) === null || _a === void 0 ? void 0 : _a.match(regex));
          if (!this._currentRoot && this._search) {
            // global search for items on root
            return matcher;
          }
          return action.parent === this._currentRoot && matcher;
        });
        const sections = actionMatches.reduce((entryMap, e) => entryMap.set(e.section, [...(entryMap.get(e.section) || []), e]), new Map());
        this._actionMatches = [...sections.values()].flat();
        if (this._actionMatches.length > 0 && this._selectedIndex === -1) {
          this._selected = this._actionMatches[0];
        }
        if (this._actionMatches.length === 0) {
          this._selected = undefined;
        }
        const actionsList = actions => (0, _lit.html)` ${(0, _repeat.repeat)(actions, action => action.id, action => {
          var _a;
          return (0, _lit.html)`<ninja-action
                exportparts="ninja-action,ninja-selected,ninja-icon"
                .selected=${(0, _live.live)(action.id === ((_a = this._selected) === null || _a === void 0 ? void 0 : _a.id))}
                .hotKeysJoinedView=${this.hotKeysJoinedView}
                @mouseover=${event => this._actionFocused(action, event)}
                @actionsSelected=${event => this._actionSelected(event.detail)}
                .action=${action}
              ></ninja-action>`;
        })}`;
        const itemTemplates = [];
        sections.forEach((actions, section) => {
          const header = section ? (0, _lit.html)`<div class="group-header">${section}</div>` : undefined;
          itemTemplates.push((0, _lit.html)`${header}${actionsList(actions)}`);
        });
        return (0, _lit.html)`
          <div @click=${this._overlayClick} class=${(0, _classMap.classMap)(menuClasses)}>
            <div class=${(0, _classMap.classMap)(classes)} @animationend=${this._onTransitionEnd}>
              <ninja-header
                exportparts="ninja-input,ninja-input-wrapper"
                ${(0, _ref.ref)(this._headerRef)}
                .placeholder=${this.placeholder}
                .hideBreadcrumbs=${this.hideBreadcrumbs}
                .breadcrumbs=${this.breadcrumbs}
                @change=${this._handleInput}
                @setParent=${event => this.setParent(event.detail.parent)}
                @close=${this.close}
              >
              </ninja-header>
              <div class="modal-body">
                <div class="actions-list" part="actions-list">${itemTemplates}</div>
              </div>
              <slot name="footer"> ${_ninjaFooter.footerHtml} </slot>
            </div>
          </div>
        `;
      }
      get _selectedIndex() {
        if (!this._selected) {
          return -1;
        }
        return this._actionMatches.indexOf(this._selected);
      }
      _actionSelected(action) {
        var _a;
        // fire selected event even when action is empty/not selected,
        // so possible handle api search for example
        this.dispatchEvent(new CustomEvent('selected', {
          detail: {
            search: this._search,
            action
          },
          bubbles: true,
          composed: true
        }));
        if (!action) {
          return;
        }
        if (action.children && ((_a = action.children) === null || _a === void 0 ? void 0 : _a.length) > 0) {
          this._currentRoot = action.id;
          this._search = '';
        }
        this._headerRef.value.setSearch('');
        this._headerRef.value.focusSearch();
        if (action.handler) {
          const result = action.handler(action);
          if (!(result === null || result === void 0 ? void 0 : result.keepOpen)) {
            this.close();
          }
        }
        this._bump = true;
      }
      async _handleInput(event) {
        this._search = event.detail.search;
        await this.updateComplete;
        this.dispatchEvent(new CustomEvent('change', {
          detail: {
            search: this._search,
            actions: this._actionMatches
          },
          bubbles: true,
          composed: true
        }));
      }
      _overlayClick(event) {
        var _a;
        if ((_a = event.target) === null || _a === void 0 ? void 0 : _a.classList.contains('modal')) {
          this.close();
        }
      }
    };
    exports.NinjaKeys = NinjaKeys;
    NinjaKeys.styles = [_baseStyles.baseStyles];
    __decorate([(0, _decorators.property)({
      type: String
    })], NinjaKeys.prototype, "placeholder", void 0);
    __decorate([(0, _decorators.property)({
      type: Boolean
    })], NinjaKeys.prototype, "disableHotkeys", void 0);
    __decorate([(0, _decorators.property)({
      type: Boolean
    })], NinjaKeys.prototype, "hideBreadcrumbs", void 0);
    __decorate([(0, _decorators.property)()], NinjaKeys.prototype, "openHotkey", void 0);
    __decorate([(0, _decorators.property)()], NinjaKeys.prototype, "navigationUpHotkey", void 0);
    __decorate([(0, _decorators.property)()], NinjaKeys.prototype, "navigationDownHotkey", void 0);
    __decorate([(0, _decorators.property)()], NinjaKeys.prototype, "closeHotkey", void 0);
    __decorate([(0, _decorators.property)()], NinjaKeys.prototype, "goBackHotkey", void 0);
    __decorate([(0, _decorators.property)()], NinjaKeys.prototype, "selectHotkey", void 0);
    __decorate([(0, _decorators.property)({
      type: Boolean
    })], NinjaKeys.prototype, "hotKeysJoinedView", void 0);
    __decorate([(0, _decorators.property)({
      type: Boolean
    })], NinjaKeys.prototype, "noAutoLoadMdIcons", void 0);
    __decorate([(0, _decorators.property)({
      type: Array,
      hasChanged() {
        // Forced to trigger changed event always.
        // Because of a lot of framework pattern wrap object with an Observer, like vue2.
        // That's why object passed to web component always same and no render triggered. Issue #9
        return true;
      }
    })], NinjaKeys.prototype, "data", void 0);
    __decorate([(0, _decorators.state)()], NinjaKeys.prototype, "visible", void 0);
    __decorate([(0, _decorators.state)()], NinjaKeys.prototype, "_bump", void 0);
    __decorate([(0, _decorators.state)()], NinjaKeys.prototype, "_actionMatches", void 0);
    __decorate([(0, _decorators.state)()], NinjaKeys.prototype, "_search", void 0);
    __decorate([(0, _decorators.state)()], NinjaKeys.prototype, "_currentRoot", void 0);
    __decorate([(0, _decorators.state)()], NinjaKeys.prototype, "_flatData", void 0);
    __decorate([(0, _decorators.state)()], NinjaKeys.prototype, "breadcrumbs", null);
    __decorate([(0, _decorators.state)()], NinjaKeys.prototype, "_selected", void 0);
    exports.NinjaKeys = NinjaKeys = __decorate([(0, _decorators.customElement)('ninja-keys')], NinjaKeys);
    
    },{"./base-styles.js":1,"./ninja-action.js":2,"./ninja-footer.js":3,"./ninja-header.js":4,"hotkeys-js":20,"lit":39,"lit-html/directives/ref.js":28,"lit/decorators.js":32,"lit/directives/class-map.js":33,"lit/directives/live.js":35,"lit/directives/repeat.js":37}],6:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    exports.unsafeCSS = exports.supportsAdoptingStyleSheets = exports.getCompatibleStyle = exports.css = exports.adoptStyles = exports.CSSResult = void 0;
    /**
     * @license
     * Copyright 2019 Google LLC
     * SPDX-License-Identifier: BSD-3-Clause
     */
    const t = window.ShadowRoot && (void 0 === window.ShadyCSS || window.ShadyCSS.nativeShadow) && "adoptedStyleSheets" in Document.prototype && "replace" in CSSStyleSheet.prototype,
      e = Symbol(),
      n = new Map();
    exports.supportsAdoptingStyleSheets = t;
    class s {
      constructor(t, n) {
        if (this._$cssResult$ = !0, n !== e) throw Error("CSSResult is not constructable. Use `unsafeCSS` or `css` instead.");
        this.cssText = t;
      }
      get styleSheet() {
        let e = n.get(this.cssText);
        return t && void 0 === e && (n.set(this.cssText, e = new CSSStyleSheet()), e.replaceSync(this.cssText)), e;
      }
      toString() {
        return this.cssText;
      }
    }
    exports.CSSResult = s;
    const o = t => new s("string" == typeof t ? t : t + "", e),
      r = (t, ...n) => {
        const o = 1 === t.length ? t[0] : n.reduce((e, n, s) => e + (t => {
          if (!0 === t._$cssResult$) return t.cssText;
          if ("number" == typeof t) return t;
          throw Error("Value passed to 'css' function must be a 'css' function result: " + t + ". Use 'unsafeCSS' to pass non-literal values, but take care to ensure page security.");
        })(n) + t[s + 1], t[0]);
        return new s(o, e);
      },
      i = (e, n) => {
        t ? e.adoptedStyleSheets = n.map(t => t instanceof CSSStyleSheet ? t : t.styleSheet) : n.forEach(t => {
          const n = document.createElement("style"),
            s = window.litNonce;
          void 0 !== s && n.setAttribute("nonce", s), n.textContent = t.cssText, e.appendChild(n);
        });
      },
      S = t ? t => t : t => t instanceof CSSStyleSheet ? (t => {
        let e = "";
        for (const n of t.cssRules) e += n.cssText;
        return o(e);
      })(t) : t;
    exports.getCompatibleStyle = S;
    exports.adoptStyles = i;
    exports.css = r;
    exports.unsafeCSS = o;
    
    },{}],7:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    exports.standardPrototypeMethod = exports.legacyPrototypeMethod = exports.decorateProperty = void 0;
    /**
     * @license
     * Copyright 2017 Google LLC
     * SPDX-License-Identifier: BSD-3-Clause
     */
    const e = (e, t, o) => {
        Object.defineProperty(t, o, e);
      },
      t = (e, t) => ({
        kind: "method",
        placement: "prototype",
        key: t.key,
        descriptor: e
      }),
      o = ({
        finisher: e,
        descriptor: t
      }) => (o, n) => {
        var r;
        if (void 0 === n) {
          const n = null !== (r = o.originalKey) && void 0 !== r ? r : o.key,
            i = null != t ? {
              kind: "method",
              placement: "prototype",
              key: n,
              descriptor: t(o.key)
            } : {
              ...o,
              key: n
            };
          return null != e && (i.finisher = function (t) {
            e(t, n);
          }), i;
        }
        {
          const r = o.constructor;
          void 0 !== t && Object.defineProperty(o, n, t(n)), null == e || e(r, n);
        }
      };
    exports.decorateProperty = o;
    exports.standardPrototypeMethod = t;
    exports.legacyPrototypeMethod = e;
    
    },{}],8:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    exports.customElement = void 0;
    /**
     * @license
     * Copyright 2017 Google LLC
     * SPDX-License-Identifier: BSD-3-Clause
     */
    const n = n => e => "function" == typeof e ? ((n, e) => (window.customElements.define(n, e), e))(n, e) : ((n, e) => {
      const {
        kind: t,
        elements: i
      } = e;
      return {
        kind: t,
        elements: i,
        finisher(e) {
          window.customElements.define(n, e);
        }
      };
    })(n, e);
    exports.customElement = n;
    
    },{}],9:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    exports.eventOptions = e;
    var _base = require("./base.js");
    /**
     * @license
     * Copyright 2017 Google LLC
     * SPDX-License-Identifier: BSD-3-Clause
     */
    function e(e) {
      return (0, _base.decorateProperty)({
        finisher: (r, t) => {
          Object.assign(r.prototype[t], e);
        }
      });
    }
    
    },{"./base.js":7}],10:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    exports.property = e;
    /**
     * @license
     * Copyright 2017 Google LLC
     * SPDX-License-Identifier: BSD-3-Clause
     */
    const i = (i, e) => "method" === e.kind && e.descriptor && !("value" in e.descriptor) ? {
      ...e,
      finisher(n) {
        n.createProperty(e.key, i);
      }
    } : {
      kind: "field",
      key: Symbol(),
      placement: "own",
      descriptor: {},
      originalKey: e.key,
      initializer() {
        "function" == typeof e.initializer && (this[e.key] = e.initializer.call(this));
      },
      finisher(n) {
        n.createProperty(e.key, i);
      }
    };
    function e(e) {
      return (n, t) => void 0 !== t ? ((i, e, n) => {
        e.constructor.createProperty(n, i);
      })(e, n, t) : i(e, n);
    }
    
    },{}],11:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    exports.queryAll = e;
    var _base = require("./base.js");
    /**
     * @license
     * Copyright 2017 Google LLC
     * SPDX-License-Identifier: BSD-3-Clause
     */
    function e(e) {
      return (0, _base.decorateProperty)({
        descriptor: r => ({
          get() {
            var r, o;
            return null !== (o = null === (r = this.renderRoot) || void 0 === r ? void 0 : r.querySelectorAll(e)) && void 0 !== o ? o : [];
          },
          enumerable: !0,
          configurable: !0
        })
      });
    }
    
    },{"./base.js":7}],12:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    exports.queryAssignedElements = l;
    var _base = require("./base.js");
    /**
     * @license
     * Copyright 2021 Google LLC
     * SPDX-License-Identifier: BSD-3-Clause
     */
    var n;
    const e = null != (null === (n = window.HTMLSlotElement) || void 0 === n ? void 0 : n.prototype.assignedElements) ? (o, n) => o.assignedElements(n) : (o, n) => o.assignedNodes(n).filter(o => o.nodeType === Node.ELEMENT_NODE);
    function l(n) {
      const {
        slot: l,
        selector: t
      } = null != n ? n : {};
      return (0, _base.decorateProperty)({
        descriptor: o => ({
          get() {
            var o;
            const r = "slot" + (l ? `[name=${l}]` : ":not([name])"),
              i = null === (o = this.renderRoot) || void 0 === o ? void 0 : o.querySelector(r),
              s = null != i ? e(i, n) : [];
            return t ? s.filter(o => o.matches(t)) : s;
          },
          enumerable: !0,
          configurable: !0
        })
      });
    }
    
    },{"./base.js":7}],13:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    exports.queryAssignedNodes = o;
    var _base = require("./base.js");
    var _queryAssignedElements = require("./query-assigned-elements.js");
    /**
     * @license
     * Copyright 2017 Google LLC
     * SPDX-License-Identifier: BSD-3-Clause
     */
    function o(o, n, r) {
      let l,
        s = o;
      return "object" == typeof o ? (s = o.slot, l = o) : l = {
        flatten: n
      }, r ? (0, _queryAssignedElements.queryAssignedElements)({
        slot: s,
        flatten: n,
        selector: r
      }) : (0, _base.decorateProperty)({
        descriptor: e => ({
          get() {
            var e, t;
            const o = "slot" + (s ? `[name=${s}]` : ":not([name])"),
              n = null === (e = this.renderRoot) || void 0 === e ? void 0 : e.querySelector(o);
            return null !== (t = null == n ? void 0 : n.assignedNodes(l)) && void 0 !== t ? t : [];
          },
          enumerable: !0,
          configurable: !0
        })
      });
    }
    
    },{"./base.js":7,"./query-assigned-elements.js":12}],14:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    exports.queryAsync = e;
    var _base = require("./base.js");
    /**
     * @license
     * Copyright 2017 Google LLC
     * SPDX-License-Identifier: BSD-3-Clause
     */
    function e(e) {
      return (0, _base.decorateProperty)({
        descriptor: r => ({
          async get() {
            var r;
            return await this.updateComplete, null === (r = this.renderRoot) || void 0 === r ? void 0 : r.querySelector(e);
          },
          enumerable: !0,
          configurable: !0
        })
      });
    }
    
    },{"./base.js":7}],15:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    exports.query = i;
    var _base = require("./base.js");
    /**
     * @license
     * Copyright 2017 Google LLC
     * SPDX-License-Identifier: BSD-3-Clause
     */
    function i(i, n) {
      return (0, _base.decorateProperty)({
        descriptor: o => {
          const t = {
            get() {
              var o, n;
              return null !== (n = null === (o = this.renderRoot) || void 0 === o ? void 0 : o.querySelector(i)) && void 0 !== n ? n : null;
            },
            enumerable: !0,
            configurable: !0
          };
          if (n) {
            const n = "symbol" == typeof o ? Symbol() : "__" + o;
            t.get = function () {
              var o, t;
              return void 0 === this[n] && (this[n] = null !== (t = null === (o = this.renderRoot) || void 0 === o ? void 0 : o.querySelector(i)) && void 0 !== t ? t : null), this[n];
            };
          }
          return t;
        }
      });
    }
    
    },{"./base.js":7}],16:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    exports.state = t;
    var _property = require("./property.js");
    /**
     * @license
     * Copyright 2017 Google LLC
     * SPDX-License-Identifier: BSD-3-Clause
     */
    function t(t) {
      return (0, _property.property)({
        ...t,
        state: !0
      });
    }
    
    },{"./property.js":10}],17:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    Object.defineProperty(exports, "CSSResult", {
      enumerable: true,
      get: function () {
        return _cssTag.CSSResult;
      }
    });
    exports.ReactiveElement = void 0;
    Object.defineProperty(exports, "adoptStyles", {
      enumerable: true,
      get: function () {
        return _cssTag.adoptStyles;
      }
    });
    Object.defineProperty(exports, "css", {
      enumerable: true,
      get: function () {
        return _cssTag.css;
      }
    });
    exports.defaultConverter = void 0;
    Object.defineProperty(exports, "getCompatibleStyle", {
      enumerable: true,
      get: function () {
        return _cssTag.getCompatibleStyle;
      }
    });
    exports.notEqual = void 0;
    Object.defineProperty(exports, "supportsAdoptingStyleSheets", {
      enumerable: true,
      get: function () {
        return _cssTag.supportsAdoptingStyleSheets;
      }
    });
    Object.defineProperty(exports, "unsafeCSS", {
      enumerable: true,
      get: function () {
        return _cssTag.unsafeCSS;
      }
    });
    var _cssTag = require("./css-tag.js");
    /**
     * @license
     * Copyright 2017 Google LLC
     * SPDX-License-Identifier: BSD-3-Clause
     */
    var s;
    const e = window.trustedTypes,
      r = e ? e.emptyScript : "",
      h = window.reactiveElementPolyfillSupport,
      o = {
        toAttribute(t, i) {
          switch (i) {
            case Boolean:
              t = t ? r : null;
              break;
            case Object:
            case Array:
              t = null == t ? t : JSON.stringify(t);
          }
          return t;
        },
        fromAttribute(t, i) {
          let s = t;
          switch (i) {
            case Boolean:
              s = null !== t;
              break;
            case Number:
              s = null === t ? null : Number(t);
              break;
            case Object:
            case Array:
              try {
                s = JSON.parse(t);
              } catch (t) {
                s = null;
              }
          }
          return s;
        }
      },
      n = (t, i) => i !== t && (i == i || t == t),
      l = {
        attribute: !0,
        type: String,
        converter: o,
        reflect: !1,
        hasChanged: n
      };
    exports.notEqual = n;
    exports.defaultConverter = o;
    class a extends HTMLElement {
      constructor() {
        super(), this._$Et = new Map(), this.isUpdatePending = !1, this.hasUpdated = !1, this._$Ei = null, this.o();
      }
      static addInitializer(t) {
        var i;
        null !== (i = this.l) && void 0 !== i || (this.l = []), this.l.push(t);
      }
      static get observedAttributes() {
        this.finalize();
        const t = [];
        return this.elementProperties.forEach((i, s) => {
          const e = this._$Eh(s, i);
          void 0 !== e && (this._$Eu.set(e, s), t.push(e));
        }), t;
      }
      static createProperty(t, i = l) {
        if (i.state && (i.attribute = !1), this.finalize(), this.elementProperties.set(t, i), !i.noAccessor && !this.prototype.hasOwnProperty(t)) {
          const s = "symbol" == typeof t ? Symbol() : "__" + t,
            e = this.getPropertyDescriptor(t, s, i);
          void 0 !== e && Object.defineProperty(this.prototype, t, e);
        }
      }
      static getPropertyDescriptor(t, i, s) {
        return {
          get() {
            return this[i];
          },
          set(e) {
            const r = this[t];
            this[i] = e, this.requestUpdate(t, r, s);
          },
          configurable: !0,
          enumerable: !0
        };
      }
      static getPropertyOptions(t) {
        return this.elementProperties.get(t) || l;
      }
      static finalize() {
        if (this.hasOwnProperty("finalized")) return !1;
        this.finalized = !0;
        const t = Object.getPrototypeOf(this);
        if (t.finalize(), this.elementProperties = new Map(t.elementProperties), this._$Eu = new Map(), this.hasOwnProperty("properties")) {
          const t = this.properties,
            i = [...Object.getOwnPropertyNames(t), ...Object.getOwnPropertySymbols(t)];
          for (const s of i) this.createProperty(s, t[s]);
        }
        return this.elementStyles = this.finalizeStyles(this.styles), !0;
      }
      static finalizeStyles(i) {
        const s = [];
        if (Array.isArray(i)) {
          const e = new Set(i.flat(1 / 0).reverse());
          for (const i of e) s.unshift((0, _cssTag.getCompatibleStyle)(i));
        } else void 0 !== i && s.push((0, _cssTag.getCompatibleStyle)(i));
        return s;
      }
      static _$Eh(t, i) {
        const s = i.attribute;
        return !1 === s ? void 0 : "string" == typeof s ? s : "string" == typeof t ? t.toLowerCase() : void 0;
      }
      o() {
        var t;
        this._$Ep = new Promise(t => this.enableUpdating = t), this._$AL = new Map(), this._$Em(), this.requestUpdate(), null === (t = this.constructor.l) || void 0 === t || t.forEach(t => t(this));
      }
      addController(t) {
        var i, s;
        (null !== (i = this._$Eg) && void 0 !== i ? i : this._$Eg = []).push(t), void 0 !== this.renderRoot && this.isConnected && (null === (s = t.hostConnected) || void 0 === s || s.call(t));
      }
      removeController(t) {
        var i;
        null === (i = this._$Eg) || void 0 === i || i.splice(this._$Eg.indexOf(t) >>> 0, 1);
      }
      _$Em() {
        this.constructor.elementProperties.forEach((t, i) => {
          this.hasOwnProperty(i) && (this._$Et.set(i, this[i]), delete this[i]);
        });
      }
      createRenderRoot() {
        var t;
        const s = null !== (t = this.shadowRoot) && void 0 !== t ? t : this.attachShadow(this.constructor.shadowRootOptions);
        return (0, _cssTag.adoptStyles)(s, this.constructor.elementStyles), s;
      }
      connectedCallback() {
        var t;
        void 0 === this.renderRoot && (this.renderRoot = this.createRenderRoot()), this.enableUpdating(!0), null === (t = this._$Eg) || void 0 === t || t.forEach(t => {
          var i;
          return null === (i = t.hostConnected) || void 0 === i ? void 0 : i.call(t);
        });
      }
      enableUpdating(t) {}
      disconnectedCallback() {
        var t;
        null === (t = this._$Eg) || void 0 === t || t.forEach(t => {
          var i;
          return null === (i = t.hostDisconnected) || void 0 === i ? void 0 : i.call(t);
        });
      }
      attributeChangedCallback(t, i, s) {
        this._$AK(t, s);
      }
      _$ES(t, i, s = l) {
        var e, r;
        const h = this.constructor._$Eh(t, s);
        if (void 0 !== h && !0 === s.reflect) {
          const n = (null !== (r = null === (e = s.converter) || void 0 === e ? void 0 : e.toAttribute) && void 0 !== r ? r : o.toAttribute)(i, s.type);
          this._$Ei = t, null == n ? this.removeAttribute(h) : this.setAttribute(h, n), this._$Ei = null;
        }
      }
      _$AK(t, i) {
        var s, e, r;
        const h = this.constructor,
          n = h._$Eu.get(t);
        if (void 0 !== n && this._$Ei !== n) {
          const t = h.getPropertyOptions(n),
            l = t.converter,
            a = null !== (r = null !== (e = null === (s = l) || void 0 === s ? void 0 : s.fromAttribute) && void 0 !== e ? e : "function" == typeof l ? l : null) && void 0 !== r ? r : o.fromAttribute;
          this._$Ei = n, this[n] = a(i, t.type), this._$Ei = null;
        }
      }
      requestUpdate(t, i, s) {
        let e = !0;
        void 0 !== t && (((s = s || this.constructor.getPropertyOptions(t)).hasChanged || n)(this[t], i) ? (this._$AL.has(t) || this._$AL.set(t, i), !0 === s.reflect && this._$Ei !== t && (void 0 === this._$EC && (this._$EC = new Map()), this._$EC.set(t, s))) : e = !1), !this.isUpdatePending && e && (this._$Ep = this._$E_());
      }
      async _$E_() {
        this.isUpdatePending = !0;
        try {
          await this._$Ep;
        } catch (t) {
          Promise.reject(t);
        }
        const t = this.scheduleUpdate();
        return null != t && (await t), !this.isUpdatePending;
      }
      scheduleUpdate() {
        return this.performUpdate();
      }
      performUpdate() {
        var t;
        if (!this.isUpdatePending) return;
        this.hasUpdated, this._$Et && (this._$Et.forEach((t, i) => this[i] = t), this._$Et = void 0);
        let i = !1;
        const s = this._$AL;
        try {
          i = this.shouldUpdate(s), i ? (this.willUpdate(s), null === (t = this._$Eg) || void 0 === t || t.forEach(t => {
            var i;
            return null === (i = t.hostUpdate) || void 0 === i ? void 0 : i.call(t);
          }), this.update(s)) : this._$EU();
        } catch (t) {
          throw i = !1, this._$EU(), t;
        }
        i && this._$AE(s);
      }
      willUpdate(t) {}
      _$AE(t) {
        var i;
        null === (i = this._$Eg) || void 0 === i || i.forEach(t => {
          var i;
          return null === (i = t.hostUpdated) || void 0 === i ? void 0 : i.call(t);
        }), this.hasUpdated || (this.hasUpdated = !0, this.firstUpdated(t)), this.updated(t);
      }
      _$EU() {
        this._$AL = new Map(), this.isUpdatePending = !1;
      }
      get updateComplete() {
        return this.getUpdateComplete();
      }
      getUpdateComplete() {
        return this._$Ep;
      }
      shouldUpdate(t) {
        return !0;
      }
      update(t) {
        void 0 !== this._$EC && (this._$EC.forEach((t, i) => this._$ES(i, this[i], t)), this._$EC = void 0), this._$EU();
      }
      updated(t) {}
      firstUpdated(t) {}
    }
    exports.ReactiveElement = a;
    a.finalized = !0, a.elementProperties = new Map(), a.elementStyles = [], a.shadowRootOptions = {
      mode: "open"
    }, null == h || h({
      ReactiveElement: a
    }), (null !== (s = globalThis.reactiveElementVersions) && void 0 !== s ? s : globalThis.reactiveElementVersions = []).push("1.3.2");
    
    },{"./css-tag.js":6}],18:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    exports.styles = void 0;
    var _lit = require("lit");
    /**
     * @license
     * Copyright 2021 Google LLC
     * SPDX-LIcense-Identifier: Apache-2.0
     */
    
    const styles = (0, _lit.css)`:host{font-family:var(--mdc-icon-font, "Material Icons");font-weight:normal;font-style:normal;font-size:var(--mdc-icon-size, 24px);line-height:1;letter-spacing:normal;text-transform:none;display:inline-block;white-space:nowrap;word-wrap:normal;direction:ltr;-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;-moz-osx-font-smoothing:grayscale;font-feature-settings:"liga"}`;
    exports.styles = styles;
    
    },{"lit":39}],19:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    exports.Icon = void 0;
    var _tslib = require("tslib");
    var _lit = require("lit");
    var _decorators = require("lit/decorators.js");
    var _mwcIconHost = require("./mwc-icon-host.css");
    /**
     * @license
     * Copyright 2018 Google LLC
     * SPDX-License-Identifier: Apache-2.0
     */
    
    // Style preference for leading underscores.
    // tslint:disable:strip-private-property-underscore
    
    /** @soyCompatible */
    let Icon = class Icon extends _lit.LitElement {
      /** @soyTemplate */
      render() {
        return (0, _lit.html)`<span><slot></slot></span>`;
      }
    };
    exports.Icon = Icon;
    Icon.styles = [_mwcIconHost.styles];
    exports.Icon = Icon = (0, _tslib.__decorate)([(0, _decorators.customElement)('mwc-icon')], Icon);
    
    },{"./mwc-icon-host.css":18,"lit":39,"lit/decorators.js":32,"tslib":40}],20:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    exports.default = void 0;
    /*!
     * hotkeys-js v3.8.7
     * A simple micro-library for defining and dispatching keyboard shortcuts. It has no dependencies.
     * 
     * Copyright (c) 2021 kenny wong <wowohoo@qq.com>
     * http://jaywcjlove.github.io/hotkeys
     * 
     * Licensed under the MIT license.
     */
    
    var isff = typeof navigator !== 'undefined' ? navigator.userAgent.toLowerCase().indexOf('firefox') > 0 : false; // 绑定事件
    
    function addEvent(object, event, method) {
      if (object.addEventListener) {
        object.addEventListener(event, method, false);
      } else if (object.attachEvent) {
        object.attachEvent("on".concat(event), function () {
          method(window.event);
        });
      }
    } // 修饰键转换成对应的键码
    
    function getMods(modifier, key) {
      var mods = key.slice(0, key.length - 1);
      for (var i = 0; i < mods.length; i++) {
        mods[i] = modifier[mods[i].toLowerCase()];
      }
      return mods;
    } // 处理传的key字符串转换成数组
    
    function getKeys(key) {
      if (typeof key !== 'string') key = '';
      key = key.replace(/\s/g, ''); // 匹配任何空白字符,包括空格、制表符、换页符等等
    
      var keys = key.split(','); // 同时设置多个快捷键，以','分割
    
      var index = keys.lastIndexOf(''); // 快捷键可能包含','，需特殊处理
    
      for (; index >= 0;) {
        keys[index - 1] += ',';
        keys.splice(index, 1);
        index = keys.lastIndexOf('');
      }
      return keys;
    } // 比较修饰键的数组
    
    function compareArray(a1, a2) {
      var arr1 = a1.length >= a2.length ? a1 : a2;
      var arr2 = a1.length >= a2.length ? a2 : a1;
      var isIndex = true;
      for (var i = 0; i < arr1.length; i++) {
        if (arr2.indexOf(arr1[i]) === -1) isIndex = false;
      }
      return isIndex;
    }
    var _keyMap = {
      backspace: 8,
      tab: 9,
      clear: 12,
      enter: 13,
      return: 13,
      esc: 27,
      escape: 27,
      space: 32,
      left: 37,
      up: 38,
      right: 39,
      down: 40,
      del: 46,
      delete: 46,
      ins: 45,
      insert: 45,
      home: 36,
      end: 35,
      pageup: 33,
      pagedown: 34,
      capslock: 20,
      num_0: 96,
      num_1: 97,
      num_2: 98,
      num_3: 99,
      num_4: 100,
      num_5: 101,
      num_6: 102,
      num_7: 103,
      num_8: 104,
      num_9: 105,
      num_multiply: 106,
      num_add: 107,
      num_enter: 108,
      num_subtract: 109,
      num_decimal: 110,
      num_divide: 111,
      '⇪': 20,
      ',': 188,
      '.': 190,
      '/': 191,
      '`': 192,
      '-': isff ? 173 : 189,
      '=': isff ? 61 : 187,
      ';': isff ? 59 : 186,
      '\'': 222,
      '[': 219,
      ']': 221,
      '\\': 220
    }; // Modifier Keys
    
    var _modifier = {
      // shiftKey
      '⇧': 16,
      shift: 16,
      // altKey
      '⌥': 18,
      alt: 18,
      option: 18,
      // ctrlKey
      '⌃': 17,
      ctrl: 17,
      control: 17,
      // metaKey
      '⌘': 91,
      cmd: 91,
      command: 91
    };
    var modifierMap = {
      16: 'shiftKey',
      18: 'altKey',
      17: 'ctrlKey',
      91: 'metaKey',
      shiftKey: 16,
      ctrlKey: 17,
      altKey: 18,
      metaKey: 91
    };
    var _mods = {
      16: false,
      18: false,
      17: false,
      91: false
    };
    var _handlers = {}; // F1~F12 special key
    
    for (var k = 1; k < 20; k++) {
      _keyMap["f".concat(k)] = 111 + k;
    }
    var _downKeys = []; // 记录摁下的绑定键
    
    var _scope = 'all'; // 默认热键范围
    
    var elementHasBindEvent = []; // 已绑定事件的节点记录
    // 返回键码
    
    var code = function code(x) {
      return _keyMap[x.toLowerCase()] || _modifier[x.toLowerCase()] || x.toUpperCase().charCodeAt(0);
    }; // 设置获取当前范围（默认为'所有'）
    
    function setScope(scope) {
      _scope = scope || 'all';
    } // 获取当前范围
    
    function getScope() {
      return _scope || 'all';
    } // 获取摁下绑定键的键值
    
    function getPressedKeyCodes() {
      return _downKeys.slice(0);
    } // 表单控件控件判断 返回 Boolean
    // hotkey is effective only when filter return true
    
    function filter(event) {
      var target = event.target || event.srcElement;
      var tagName = target.tagName;
      var flag = true; // ignore: isContentEditable === 'true', <input> and <textarea> when readOnly state is false, <select>
    
      if (target.isContentEditable || (tagName === 'INPUT' || tagName === 'TEXTAREA' || tagName === 'SELECT') && !target.readOnly) {
        flag = false;
      }
      return flag;
    } // 判断摁下的键是否为某个键，返回true或者false
    
    function isPressed(keyCode) {
      if (typeof keyCode === 'string') {
        keyCode = code(keyCode); // 转换成键码
      }
    
      return _downKeys.indexOf(keyCode) !== -1;
    } // 循环删除handlers中的所有 scope(范围)
    
    function deleteScope(scope, newScope) {
      var handlers;
      var i; // 没有指定scope，获取scope
    
      if (!scope) scope = getScope();
      for (var key in _handlers) {
        if (Object.prototype.hasOwnProperty.call(_handlers, key)) {
          handlers = _handlers[key];
          for (i = 0; i < handlers.length;) {
            if (handlers[i].scope === scope) handlers.splice(i, 1);else i++;
          }
        }
      } // 如果scope被删除，将scope重置为all
    
      if (getScope() === scope) setScope(newScope || 'all');
    } // 清除修饰键
    
    function clearModifier(event) {
      var key = event.keyCode || event.which || event.charCode;
      var i = _downKeys.indexOf(key); // 从列表中清除按压过的键
    
      if (i >= 0) {
        _downKeys.splice(i, 1);
      } // 特殊处理 cmmand 键，在 cmmand 组合快捷键 keyup 只执行一次的问题
    
      if (event.key && event.key.toLowerCase() === 'meta') {
        _downKeys.splice(0, _downKeys.length);
      } // 修饰键 shiftKey altKey ctrlKey (command||metaKey) 清除
    
      if (key === 93 || key === 224) key = 91;
      if (key in _mods) {
        _mods[key] = false; // 将修饰键重置为false
    
        for (var k in _modifier) {
          if (_modifier[k] === key) hotkeys[k] = false;
        }
      }
    }
    function unbind(keysInfo) {
      // unbind(), unbind all keys
      if (!keysInfo) {
        Object.keys(_handlers).forEach(function (key) {
          return delete _handlers[key];
        });
      } else if (Array.isArray(keysInfo)) {
        // support like : unbind([{key: 'ctrl+a', scope: 's1'}, {key: 'ctrl-a', scope: 's2', splitKey: '-'}])
        keysInfo.forEach(function (info) {
          if (info.key) eachUnbind(info);
        });
      } else if (typeof keysInfo === 'object') {
        // support like unbind({key: 'ctrl+a, ctrl+b', scope:'abc'})
        if (keysInfo.key) eachUnbind(keysInfo);
      } else if (typeof keysInfo === 'string') {
        for (var _len = arguments.length, args = new Array(_len > 1 ? _len - 1 : 0), _key = 1; _key < _len; _key++) {
          args[_key - 1] = arguments[_key];
        }
    
        // support old method
        // eslint-disable-line
        var scope = args[0],
          method = args[1];
        if (typeof scope === 'function') {
          method = scope;
          scope = '';
        }
        eachUnbind({
          key: keysInfo,
          scope: scope,
          method: method,
          splitKey: '+'
        });
      }
    } // 解除绑定某个范围的快捷键
    
    var eachUnbind = function eachUnbind(_ref) {
      var key = _ref.key,
        scope = _ref.scope,
        method = _ref.method,
        _ref$splitKey = _ref.splitKey,
        splitKey = _ref$splitKey === void 0 ? '+' : _ref$splitKey;
      var multipleKeys = getKeys(key);
      multipleKeys.forEach(function (originKey) {
        var unbindKeys = originKey.split(splitKey);
        var len = unbindKeys.length;
        var lastKey = unbindKeys[len - 1];
        var keyCode = lastKey === '*' ? '*' : code(lastKey);
        if (!_handlers[keyCode]) return; // 判断是否传入范围，没有就获取范围
    
        if (!scope) scope = getScope();
        var mods = len > 1 ? getMods(_modifier, unbindKeys) : [];
        _handlers[keyCode] = _handlers[keyCode].map(function (record) {
          // 通过函数判断，是否解除绑定，函数相等直接返回
          var isMatchingMethod = method ? record.method === method : true;
          if (isMatchingMethod && record.scope === scope && compareArray(record.mods, mods)) {
            return {};
          }
          return record;
        });
      });
    }; // 对监听对应快捷键的回调函数进行处理
    
    function eventHandler(event, handler, scope) {
      var modifiersMatch; // 看它是否在当前范围
    
      if (handler.scope === scope || handler.scope === 'all') {
        // 检查是否匹配修饰符（如果有返回true）
        modifiersMatch = handler.mods.length > 0;
        for (var y in _mods) {
          if (Object.prototype.hasOwnProperty.call(_mods, y)) {
            if (!_mods[y] && handler.mods.indexOf(+y) > -1 || _mods[y] && handler.mods.indexOf(+y) === -1) {
              modifiersMatch = false;
            }
          }
        } // 调用处理程序，如果是修饰键不做处理
    
        if (handler.mods.length === 0 && !_mods[16] && !_mods[18] && !_mods[17] && !_mods[91] || modifiersMatch || handler.shortcut === '*') {
          if (handler.method(event, handler) === false) {
            if (event.preventDefault) event.preventDefault();else event.returnValue = false;
            if (event.stopPropagation) event.stopPropagation();
            if (event.cancelBubble) event.cancelBubble = true;
          }
        }
      }
    } // 处理keydown事件
    
    function dispatch(event) {
      var asterisk = _handlers['*'];
      var key = event.keyCode || event.which || event.charCode; // 表单控件过滤 默认表单控件不触发快捷键
    
      if (!hotkeys.filter.call(this, event)) return; // Gecko(Firefox)的command键值224，在Webkit(Chrome)中保持一致
      // Webkit左右 command 键值不一样
    
      if (key === 93 || key === 224) key = 91;
      /**
       * Collect bound keys
       * If an Input Method Editor is processing key input and the event is keydown, return 229.
       * https://stackoverflow.com/questions/25043934/is-it-ok-to-ignore-keydown-events-with-keycode-229
       * http://lists.w3.org/Archives/Public/www-dom/2010JulSep/att-0182/keyCode-spec.html
       */
    
      if (_downKeys.indexOf(key) === -1 && key !== 229) _downKeys.push(key);
      /**
       * Jest test cases are required.
       * ===============================
       */
    
      ['ctrlKey', 'altKey', 'shiftKey', 'metaKey'].forEach(function (keyName) {
        var keyNum = modifierMap[keyName];
        if (event[keyName] && _downKeys.indexOf(keyNum) === -1) {
          _downKeys.push(keyNum);
        } else if (!event[keyName] && _downKeys.indexOf(keyNum) > -1) {
          _downKeys.splice(_downKeys.indexOf(keyNum), 1);
        } else if (keyName === 'metaKey' && event[keyName] && _downKeys.length === 3) {
          /**
           * Fix if Command is pressed:
           * ===============================
           */
          if (!(event.ctrlKey || event.shiftKey || event.altKey)) {
            _downKeys = _downKeys.slice(_downKeys.indexOf(keyNum));
          }
        }
      });
      /**
       * -------------------------------
       */
    
      if (key in _mods) {
        _mods[key] = true; // 将特殊字符的key注册到 hotkeys 上
    
        for (var k in _modifier) {
          if (_modifier[k] === key) hotkeys[k] = true;
        }
        if (!asterisk) return;
      } // 将 modifierMap 里面的修饰键绑定到 event 中
    
      for (var e in _mods) {
        if (Object.prototype.hasOwnProperty.call(_mods, e)) {
          _mods[e] = event[modifierMap[e]];
        }
      }
      /**
       * https://github.com/jaywcjlove/hotkeys/pull/129
       * This solves the issue in Firefox on Windows where hotkeys corresponding to special characters would not trigger.
       * An example of this is ctrl+alt+m on a Swedish keyboard which is used to type μ.
       * Browser support: https://caniuse.com/#feat=keyboardevent-getmodifierstate
       */
    
      if (event.getModifierState && !(event.altKey && !event.ctrlKey) && event.getModifierState('AltGraph')) {
        if (_downKeys.indexOf(17) === -1) {
          _downKeys.push(17);
        }
        if (_downKeys.indexOf(18) === -1) {
          _downKeys.push(18);
        }
        _mods[17] = true;
        _mods[18] = true;
      } // 获取范围 默认为 `all`
    
      var scope = getScope(); // 对任何快捷键都需要做的处理
    
      if (asterisk) {
        for (var i = 0; i < asterisk.length; i++) {
          if (asterisk[i].scope === scope && (event.type === 'keydown' && asterisk[i].keydown || event.type === 'keyup' && asterisk[i].keyup)) {
            eventHandler(event, asterisk[i], scope);
          }
        }
      } // key 不在 _handlers 中返回
    
      if (!(key in _handlers)) return;
      for (var _i = 0; _i < _handlers[key].length; _i++) {
        if (event.type === 'keydown' && _handlers[key][_i].keydown || event.type === 'keyup' && _handlers[key][_i].keyup) {
          if (_handlers[key][_i].key) {
            var record = _handlers[key][_i];
            var splitKey = record.splitKey;
            var keyShortcut = record.key.split(splitKey);
            var _downKeysCurrent = []; // 记录当前按键键值
    
            for (var a = 0; a < keyShortcut.length; a++) {
              _downKeysCurrent.push(code(keyShortcut[a]));
            }
            if (_downKeysCurrent.sort().join('') === _downKeys.sort().join('')) {
              // 找到处理内容
              eventHandler(event, record, scope);
            }
          }
        }
      }
    } // 判断 element 是否已经绑定事件
    
    function isElementBind(element) {
      return elementHasBindEvent.indexOf(element) > -1;
    }
    function hotkeys(key, option, method) {
      _downKeys = [];
      var keys = getKeys(key); // 需要处理的快捷键列表
    
      var mods = [];
      var scope = 'all'; // scope默认为all，所有范围都有效
    
      var element = document; // 快捷键事件绑定节点
    
      var i = 0;
      var keyup = false;
      var keydown = true;
      var splitKey = '+'; // 对为设定范围的判断
    
      if (method === undefined && typeof option === 'function') {
        method = option;
      }
      if (Object.prototype.toString.call(option) === '[object Object]') {
        if (option.scope) scope = option.scope; // eslint-disable-line
    
        if (option.element) element = option.element; // eslint-disable-line
    
        if (option.keyup) keyup = option.keyup; // eslint-disable-line
    
        if (option.keydown !== undefined) keydown = option.keydown; // eslint-disable-line
    
        if (typeof option.splitKey === 'string') splitKey = option.splitKey; // eslint-disable-line
      }
    
      if (typeof option === 'string') scope = option; // 对于每个快捷键进行处理
    
      for (; i < keys.length; i++) {
        key = keys[i].split(splitKey); // 按键列表
    
        mods = []; // 如果是组合快捷键取得组合快捷键
    
        if (key.length > 1) mods = getMods(_modifier, key); // 将非修饰键转化为键码
    
        key = key[key.length - 1];
        key = key === '*' ? '*' : code(key); // *表示匹配所有快捷键
        // 判断key是否在_handlers中，不在就赋一个空数组
    
        if (!(key in _handlers)) _handlers[key] = [];
        _handlers[key].push({
          keyup: keyup,
          keydown: keydown,
          scope: scope,
          mods: mods,
          shortcut: keys[i],
          method: method,
          key: keys[i],
          splitKey: splitKey
        });
      } // 在全局document上设置快捷键
    
      if (typeof element !== 'undefined' && !isElementBind(element) && window) {
        elementHasBindEvent.push(element);
        addEvent(element, 'keydown', function (e) {
          dispatch(e);
        });
        addEvent(window, 'focus', function () {
          _downKeys = [];
        });
        addEvent(element, 'keyup', function (e) {
          dispatch(e);
          clearModifier(e);
        });
      }
    }
    var _api = {
      setScope: setScope,
      getScope: getScope,
      deleteScope: deleteScope,
      getPressedKeyCodes: getPressedKeyCodes,
      isPressed: isPressed,
      filter: filter,
      unbind: unbind
    };
    for (var a in _api) {
      if (Object.prototype.hasOwnProperty.call(_api, a)) {
        hotkeys[a] = _api[a];
      }
    }
    if (typeof window !== 'undefined') {
      var _hotkeys = window.hotkeys;
      hotkeys.noConflict = function (deep) {
        if (deep && window.hotkeys === hotkeys) {
          window.hotkeys = _hotkeys;
        }
        return hotkeys;
      };
      window.hotkeys = hotkeys;
    }
    var _default = hotkeys;
    exports.default = _default;
    
    },{}],21:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    var _exportNames = {
      LitElement: true,
      UpdatingElement: true,
      _$LE: true
    };
    exports._$LE = exports.UpdatingElement = exports.LitElement = void 0;
    var _reactiveElement = require("@lit/reactive-element");
    Object.keys(_reactiveElement).forEach(function (key) {
      if (key === "default" || key === "__esModule") return;
      if (Object.prototype.hasOwnProperty.call(_exportNames, key)) return;
      if (key in exports && exports[key] === _reactiveElement[key]) return;
      Object.defineProperty(exports, key, {
        enumerable: true,
        get: function () {
          return _reactiveElement[key];
        }
      });
    });
    var _litHtml = require("lit-html");
    Object.keys(_litHtml).forEach(function (key) {
      if (key === "default" || key === "__esModule") return;
      if (Object.prototype.hasOwnProperty.call(_exportNames, key)) return;
      if (key in exports && exports[key] === _litHtml[key]) return;
      Object.defineProperty(exports, key, {
        enumerable: true,
        get: function () {
          return _litHtml[key];
        }
      });
    });
    /**
     * @license
     * Copyright 2017 Google LLC
     * SPDX-License-Identifier: BSD-3-Clause
     */
    var l, o;
    const r = _reactiveElement.ReactiveElement;
    exports.UpdatingElement = r;
    class s extends _reactiveElement.ReactiveElement {
      constructor() {
        super(...arguments), this.renderOptions = {
          host: this
        }, this._$Dt = void 0;
      }
      createRenderRoot() {
        var t, e;
        const i = super.createRenderRoot();
        return null !== (t = (e = this.renderOptions).renderBefore) && void 0 !== t || (e.renderBefore = i.firstChild), i;
      }
      update(t) {
        const i = this.render();
        this.hasUpdated || (this.renderOptions.isConnected = this.isConnected), super.update(t), this._$Dt = (0, _litHtml.render)(i, this.renderRoot, this.renderOptions);
      }
      connectedCallback() {
        var t;
        super.connectedCallback(), null === (t = this._$Dt) || void 0 === t || t.setConnected(!0);
      }
      disconnectedCallback() {
        var t;
        super.disconnectedCallback(), null === (t = this._$Dt) || void 0 === t || t.setConnected(!1);
      }
      render() {
        return _litHtml.noChange;
      }
    }
    exports.LitElement = s;
    s.finalized = !0, s._$litElement$ = !0, null === (l = globalThis.litElementHydrateSupport) || void 0 === l || l.call(globalThis, {
      LitElement: s
    });
    const n = globalThis.litElementPolyfillSupport;
    null == n || n({
      LitElement: s
    });
    const h = {
      _$AK: (t, e, i) => {
        t._$AK(e, i);
      },
      _$AL: t => t._$AL
    };
    exports._$LE = h;
    (null !== (o = globalThis.litElementVersions) && void 0 !== o ? o : globalThis.litElementVersions = []).push("3.2.0");
    
    },{"@lit/reactive-element":17,"lit-html":31}],22:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    exports.AsyncDirective = void 0;
    Object.defineProperty(exports, "directive", {
      enumerable: true,
      get: function () {
        return _directive.directive;
      }
    });
    var _directiveHelpers = require("./directive-helpers.js");
    var _directive = require("./directive.js");
    /**
     * @license
     * Copyright 2017 Google LLC
     * SPDX-License-Identifier: BSD-3-Clause
     */
    const e = (i, t) => {
        var s, o;
        const n = i._$AN;
        if (void 0 === n) return !1;
        for (const i of n) null === (o = (s = i)._$AO) || void 0 === o || o.call(s, t, !1), e(i, t);
        return !0;
      },
      o = i => {
        let t, s;
        do {
          if (void 0 === (t = i._$AM)) break;
          s = t._$AN, s.delete(i), i = t;
        } while (0 === (null == s ? void 0 : s.size));
      },
      n = i => {
        for (let t; t = i._$AM; i = t) {
          let s = t._$AN;
          if (void 0 === s) t._$AN = s = new Set();else if (s.has(i)) break;
          s.add(i), l(t);
        }
      };
    function r(i) {
      void 0 !== this._$AN ? (o(this), this._$AM = i, n(this)) : this._$AM = i;
    }
    function h(i, t = !1, s = 0) {
      const n = this._$AH,
        r = this._$AN;
      if (void 0 !== r && 0 !== r.size) if (t) {
        if (Array.isArray(n)) for (let i = s; i < n.length; i++) e(n[i], !1), o(n[i]);else null != n && (e(n, !1), o(n));
      } else e(this, i);
    }
    const l = i => {
      var t, e, o, n;
      i.type == _directive.PartType.CHILD && (null !== (t = (o = i)._$AP) && void 0 !== t || (o._$AP = h), null !== (e = (n = i)._$AQ) && void 0 !== e || (n._$AQ = r));
    };
    class d extends _directive.Directive {
      constructor() {
        super(...arguments), this._$AN = void 0;
      }
      _$AT(i, t, s) {
        super._$AT(i, t, s), n(this), this.isConnected = i._$AU;
      }
      _$AO(i, t = !0) {
        var s, n;
        i !== this.isConnected && (this.isConnected = i, i ? null === (s = this.reconnected) || void 0 === s || s.call(this) : null === (n = this.disconnected) || void 0 === n || n.call(this)), t && (e(this, i), o(this));
      }
      setValue(t) {
        if ((0, _directiveHelpers.isSingleExpression)(this._$Ct)) this._$Ct._$AI(t, this);else {
          const i = [...this._$Ct._$AH];
          i[this._$Ci] = t, this._$Ct._$AI(i, this, 0);
        }
      }
      disconnected() {}
      reconnected() {}
    }
    exports.AsyncDirective = d;
    
    },{"./directive-helpers.js":23,"./directive.js":24}],23:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    exports.setCommittedValue = exports.setChildPartValue = exports.removePart = exports.isTemplateResult = exports.isSingleExpression = exports.isPrimitive = exports.isDirectiveResult = exports.insertPart = exports.getDirectiveClass = exports.getCommittedValue = exports.clearPart = exports.TemplateResultType = void 0;
    var _litHtml = require("./lit-html.js");
    /**
     * @license
     * Copyright 2020 Google LLC
     * SPDX-License-Identifier: BSD-3-Clause
     */
    const {
        H: i
      } = _litHtml._$LH,
      t = o => null === o || "object" != typeof o && "function" != typeof o,
      n = {
        HTML: 1,
        SVG: 2
      },
      v = (o, i) => {
        var t, n;
        return void 0 === i ? void 0 !== (null === (t = o) || void 0 === t ? void 0 : t._$litType$) : (null === (n = o) || void 0 === n ? void 0 : n._$litType$) === i;
      },
      l = o => {
        var i;
        return void 0 !== (null === (i = o) || void 0 === i ? void 0 : i._$litDirective$);
      },
      d = o => {
        var i;
        return null === (i = o) || void 0 === i ? void 0 : i._$litDirective$;
      },
      r = o => void 0 === o.strings,
      e = () => document.createComment(""),
      u = (o, t, n) => {
        var v;
        const l = o._$AA.parentNode,
          d = void 0 === t ? o._$AB : t._$AA;
        if (void 0 === n) {
          const t = l.insertBefore(e(), d),
            v = l.insertBefore(e(), d);
          n = new i(t, v, o, o.options);
        } else {
          const i = n._$AB.nextSibling,
            t = n._$AM,
            r = t !== o;
          if (r) {
            let i;
            null === (v = n._$AQ) || void 0 === v || v.call(n, o), n._$AM = o, void 0 !== n._$AP && (i = o._$AU) !== t._$AU && n._$AP(i);
          }
          if (i !== d || r) {
            let o = n._$AA;
            for (; o !== i;) {
              const i = o.nextSibling;
              l.insertBefore(o, d), o = i;
            }
          }
        }
        return n;
      },
      c = (o, i, t = o) => (o._$AI(i, t), o),
      f = {},
      s = (o, i = f) => o._$AH = i,
      a = o => o._$AH,
      m = o => {
        var i;
        null === (i = o._$AP) || void 0 === i || i.call(o, !1, !0);
        let t = o._$AA;
        const n = o._$AB.nextSibling;
        for (; t !== n;) {
          const o = t.nextSibling;
          t.remove(), t = o;
        }
      },
      p = o => {
        o._$AR();
      };
    exports.clearPart = p;
    exports.removePart = m;
    exports.getCommittedValue = a;
    exports.setCommittedValue = s;
    exports.setChildPartValue = c;
    exports.insertPart = u;
    exports.isSingleExpression = r;
    exports.getDirectiveClass = d;
    exports.isDirectiveResult = l;
    exports.isTemplateResult = v;
    exports.TemplateResultType = n;
    exports.isPrimitive = t;
    
    },{"./lit-html.js":31}],24:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    exports.directive = exports.PartType = exports.Directive = void 0;
    /**
     * @license
     * Copyright 2017 Google LLC
     * SPDX-License-Identifier: BSD-3-Clause
     */
    const t = {
        ATTRIBUTE: 1,
        CHILD: 2,
        PROPERTY: 3,
        BOOLEAN_ATTRIBUTE: 4,
        EVENT: 5,
        ELEMENT: 6
      },
      e = t => (...e) => ({
        _$litDirective$: t,
        values: e
      });
    exports.directive = e;
    exports.PartType = t;
    class i {
      constructor(t) {}
      get _$AU() {
        return this._$AM._$AU;
      }
      _$AT(t, e, i) {
        this._$Ct = t, this._$AM = e, this._$Ci = i;
      }
      _$AS(t, e) {
        return this.update(t, e);
      }
      update(t, e) {
        return this.render(...e);
      }
    }
    exports.Directive = i;
    
    },{}],25:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    exports.classMap = void 0;
    var _litHtml = require("../lit-html.js");
    var _directive = require("../directive.js");
    /**
     * @license
     * Copyright 2018 Google LLC
     * SPDX-License-Identifier: BSD-3-Clause
     */
    const o = (0, _directive.directive)(class extends _directive.Directive {
      constructor(t) {
        var i;
        if (super(t), t.type !== _directive.PartType.ATTRIBUTE || "class" !== t.name || (null === (i = t.strings) || void 0 === i ? void 0 : i.length) > 2) throw Error("`classMap()` can only be used in the `class` attribute and must be the only part in the attribute.");
      }
      render(t) {
        return " " + Object.keys(t).filter(i => t[i]).join(" ") + " ";
      }
      update(i, [s]) {
        var r, o;
        if (void 0 === this.et) {
          this.et = new Set(), void 0 !== i.strings && (this.st = new Set(i.strings.join(" ").split(/\s/).filter(t => "" !== t)));
          for (const t in s) s[t] && !(null === (r = this.st) || void 0 === r ? void 0 : r.has(t)) && this.et.add(t);
          return this.render(s);
        }
        const e = i.element.classList;
        this.et.forEach(t => {
          t in s || (e.remove(t), this.et.delete(t));
        });
        for (const t in s) {
          const i = !!s[t];
          i === this.et.has(t) || (null === (o = this.st) || void 0 === o ? void 0 : o.has(t)) || (i ? (e.add(t), this.et.add(t)) : (e.remove(t), this.et.delete(t)));
        }
        return _litHtml.noChange;
      }
    });
    exports.classMap = o;
    
    },{"../directive.js":24,"../lit-html.js":31}],26:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    exports.join = o;
    /**
     * @license
     * Copyright 2021 Google LLC
     * SPDX-License-Identifier: BSD-3-Clause
     */
    function* o(o, t) {
      const f = "function" == typeof t;
      if (void 0 !== o) {
        let i = -1;
        for (const n of o) i > -1 && (yield f ? t(i) : t), i++, yield n;
      }
    }
    
    },{}],27:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    exports.live = void 0;
    var _litHtml = require("../lit-html.js");
    var _directive = require("../directive.js");
    var _directiveHelpers = require("../directive-helpers.js");
    /**
     * @license
     * Copyright 2020 Google LLC
     * SPDX-License-Identifier: BSD-3-Clause
     */
    const l = (0, _directive.directive)(class extends _directive.Directive {
      constructor(r) {
        if (super(r), r.type !== _directive.PartType.PROPERTY && r.type !== _directive.PartType.ATTRIBUTE && r.type !== _directive.PartType.BOOLEAN_ATTRIBUTE) throw Error("The `live` directive is not allowed on child or event bindings");
        if (!(0, _directiveHelpers.isSingleExpression)(r)) throw Error("`live` bindings can only contain a single expression");
      }
      render(r) {
        return r;
      }
      update(i, [t]) {
        if (t === _litHtml.noChange || t === _litHtml.nothing) return t;
        const o = i.element,
          l = i.name;
        if (i.type === _directive.PartType.PROPERTY) {
          if (t === o[l]) return _litHtml.noChange;
        } else if (i.type === _directive.PartType.BOOLEAN_ATTRIBUTE) {
          if (!!t === o.hasAttribute(l)) return _litHtml.noChange;
        } else if (i.type === _directive.PartType.ATTRIBUTE && o.getAttribute(l) === t + "") return _litHtml.noChange;
        return (0, _directiveHelpers.setCommittedValue)(i), t;
      }
    });
    exports.live = l;
    
    },{"../directive-helpers.js":23,"../directive.js":24,"../lit-html.js":31}],28:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    exports.ref = exports.createRef = void 0;
    var _litHtml = require("../lit-html.js");
    var _asyncDirective = require("../async-directive.js");
    var _directive = require("../directive.js");
    /**
     * @license
     * Copyright 2020 Google LLC
     * SPDX-License-Identifier: BSD-3-Clause
     */
    const e = () => new o();
    exports.createRef = e;
    class o {}
    const h = new WeakMap(),
      n = (0, _directive.directive)(class extends _asyncDirective.AsyncDirective {
        render(t) {
          return _litHtml.nothing;
        }
        update(t, [s]) {
          var e;
          const o = s !== this.U;
          return o && void 0 !== this.U && this.ot(void 0), (o || this.rt !== this.lt) && (this.U = s, this.ht = null === (e = t.options) || void 0 === e ? void 0 : e.host, this.ot(this.lt = t.element)), _litHtml.nothing;
        }
        ot(i) {
          var t;
          if ("function" == typeof this.U) {
            const s = null !== (t = this.ht) && void 0 !== t ? t : globalThis;
            let e = h.get(s);
            void 0 === e && (e = new WeakMap(), h.set(s, e)), void 0 !== e.get(this.U) && this.U.call(this.ht, void 0), e.set(this.U, i), void 0 !== i && this.U.call(this.ht, i);
          } else this.U.value = i;
        }
        get rt() {
          var i, t, s;
          return "function" == typeof this.U ? null === (t = h.get(null !== (i = this.ht) && void 0 !== i ? i : globalThis)) || void 0 === t ? void 0 : t.get(this.U) : null === (s = this.U) || void 0 === s ? void 0 : s.value;
        }
        disconnected() {
          this.rt === this.lt && this.ot(void 0);
        }
        reconnected() {
          this.ot(this.lt);
        }
      });
    exports.ref = n;
    
    },{"../async-directive.js":22,"../directive.js":24,"../lit-html.js":31}],29:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    exports.repeat = void 0;
    var _litHtml = require("../lit-html.js");
    var _directive = require("../directive.js");
    var _directiveHelpers = require("../directive-helpers.js");
    /**
     * @license
     * Copyright 2017 Google LLC
     * SPDX-License-Identifier: BSD-3-Clause
     */
    const u = (e, s, t) => {
        const r = new Map();
        for (let l = s; l <= t; l++) r.set(e[l], l);
        return r;
      },
      c = (0, _directive.directive)(class extends _directive.Directive {
        constructor(e) {
          if (super(e), e.type !== _directive.PartType.CHILD) throw Error("repeat() can only be used in text expressions");
        }
        dt(e, s, t) {
          let r;
          void 0 === t ? t = s : void 0 !== s && (r = s);
          const l = [],
            o = [];
          let i = 0;
          for (const s of e) l[i] = r ? r(s, i) : i, o[i] = t(s, i), i++;
          return {
            values: o,
            keys: l
          };
        }
        render(e, s, t) {
          return this.dt(e, s, t).values;
        }
        update(s, [t, r, c]) {
          var d;
          const a = (0, _directiveHelpers.getCommittedValue)(s),
            {
              values: p,
              keys: v
            } = this.dt(t, r, c);
          if (!Array.isArray(a)) return this.ut = v, p;
          const h = null !== (d = this.ut) && void 0 !== d ? d : this.ut = [],
            m = [];
          let y,
            x,
            j = 0,
            k = a.length - 1,
            w = 0,
            A = p.length - 1;
          for (; j <= k && w <= A;) if (null === a[j]) j++;else if (null === a[k]) k--;else if (h[j] === v[w]) m[w] = (0, _directiveHelpers.setChildPartValue)(a[j], p[w]), j++, w++;else if (h[k] === v[A]) m[A] = (0, _directiveHelpers.setChildPartValue)(a[k], p[A]), k--, A--;else if (h[j] === v[A]) m[A] = (0, _directiveHelpers.setChildPartValue)(a[j], p[A]), (0, _directiveHelpers.insertPart)(s, m[A + 1], a[j]), j++, A--;else if (h[k] === v[w]) m[w] = (0, _directiveHelpers.setChildPartValue)(a[k], p[w]), (0, _directiveHelpers.insertPart)(s, a[j], a[k]), k--, w++;else if (void 0 === y && (y = u(v, w, A), x = u(h, j, k)), y.has(h[j])) {
            if (y.has(h[k])) {
              const e = x.get(v[w]),
                t = void 0 !== e ? a[e] : null;
              if (null === t) {
                const e = (0, _directiveHelpers.insertPart)(s, a[j]);
                (0, _directiveHelpers.setChildPartValue)(e, p[w]), m[w] = e;
              } else m[w] = (0, _directiveHelpers.setChildPartValue)(t, p[w]), (0, _directiveHelpers.insertPart)(s, a[j], t), a[e] = null;
              w++;
            } else (0, _directiveHelpers.removePart)(a[k]), k--;
          } else (0, _directiveHelpers.removePart)(a[j]), j++;
          for (; w <= A;) {
            const e = (0, _directiveHelpers.insertPart)(s, m[A + 1]);
            (0, _directiveHelpers.setChildPartValue)(e, p[w]), m[w++] = e;
          }
          for (; j <= k;) {
            const e = a[j++];
            null !== e && (0, _directiveHelpers.removePart)(e);
          }
          return this.ut = v, (0, _directiveHelpers.setCommittedValue)(s, m), _litHtml.noChange;
        }
      });
    exports.repeat = c;
    
    },{"../directive-helpers.js":23,"../directive.js":24,"../lit-html.js":31}],30:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    exports.unsafeHTML = exports.UnsafeHTMLDirective = void 0;
    var _litHtml = require("../lit-html.js");
    var _directive = require("../directive.js");
    /**
     * @license
     * Copyright 2017 Google LLC
     * SPDX-License-Identifier: BSD-3-Clause
     */
    class e extends _directive.Directive {
      constructor(i) {
        if (super(i), this.it = _litHtml.nothing, i.type !== _directive.PartType.CHILD) throw Error(this.constructor.directiveName + "() can only be used in child bindings");
      }
      render(r) {
        if (r === _litHtml.nothing || null == r) return this.ft = void 0, this.it = r;
        if (r === _litHtml.noChange) return r;
        if ("string" != typeof r) throw Error(this.constructor.directiveName + "() called with a non-string value");
        if (r === this.it) return this.ft;
        this.it = r;
        const s = [r];
        return s.raw = s, this.ft = {
          _$litType$: this.constructor.resultType,
          strings: s,
          values: []
        };
      }
    }
    exports.UnsafeHTMLDirective = e;
    e.directiveName = "unsafeHTML", e.resultType = 1;
    const o = (0, _directive.directive)(e);
    exports.unsafeHTML = o;
    
    },{"../directive.js":24,"../lit-html.js":31}],31:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    exports.svg = exports.render = exports.nothing = exports.noChange = exports.html = exports._$LH = void 0;
    /**
     * @license
     * Copyright 2017 Google LLC
     * SPDX-License-Identifier: BSD-3-Clause
     */
    var t;
    const i = globalThis.trustedTypes,
      s = i ? i.createPolicy("lit-html", {
        createHTML: t => t
      }) : void 0,
      e = `lit$${(Math.random() + "").slice(9)}$`,
      o = "?" + e,
      n = `<${o}>`,
      l = document,
      h = (t = "") => l.createComment(t),
      r = t => null === t || "object" != typeof t && "function" != typeof t,
      d = Array.isArray,
      u = t => {
        var i;
        return d(t) || "function" == typeof (null === (i = t) || void 0 === i ? void 0 : i[Symbol.iterator]);
      },
      c = /<(?:(!--|\/[^a-zA-Z])|(\/?[a-zA-Z][^>\s]*)|(\/?$))/g,
      v = /-->/g,
      a = />/g,
      f = />|[ 	\n\r](?:([^\s"'>=/]+)([ 	\n\r]*=[ 	\n\r]*(?:[^ 	\n\r"'`<>=]|("|')|))|$)/g,
      _ = /'/g,
      m = /"/g,
      g = /^(?:script|style|textarea|title)$/i,
      p = t => (i, ...s) => ({
        _$litType$: t,
        strings: i,
        values: s
      }),
      $ = p(1),
      y = p(2),
      b = Symbol.for("lit-noChange"),
      w = Symbol.for("lit-nothing"),
      T = new WeakMap(),
      x = (t, i, s) => {
        var e, o;
        const n = null !== (e = null == s ? void 0 : s.renderBefore) && void 0 !== e ? e : i;
        let l = n._$litPart$;
        if (void 0 === l) {
          const t = null !== (o = null == s ? void 0 : s.renderBefore) && void 0 !== o ? o : null;
          n._$litPart$ = l = new N(i.insertBefore(h(), t), t, void 0, null != s ? s : {});
        }
        return l._$AI(t), l;
      },
      A = l.createTreeWalker(l, 129, null, !1),
      C = (t, i) => {
        const o = t.length - 1,
          l = [];
        let h,
          r = 2 === i ? "<svg>" : "",
          d = c;
        for (let i = 0; i < o; i++) {
          const s = t[i];
          let o,
            u,
            p = -1,
            $ = 0;
          for (; $ < s.length && (d.lastIndex = $, u = d.exec(s), null !== u);) $ = d.lastIndex, d === c ? "!--" === u[1] ? d = v : void 0 !== u[1] ? d = a : void 0 !== u[2] ? (g.test(u[2]) && (h = RegExp("</" + u[2], "g")), d = f) : void 0 !== u[3] && (d = f) : d === f ? ">" === u[0] ? (d = null != h ? h : c, p = -1) : void 0 === u[1] ? p = -2 : (p = d.lastIndex - u[2].length, o = u[1], d = void 0 === u[3] ? f : '"' === u[3] ? m : _) : d === m || d === _ ? d = f : d === v || d === a ? d = c : (d = f, h = void 0);
          const y = d === f && t[i + 1].startsWith("/>") ? " " : "";
          r += d === c ? s + n : p >= 0 ? (l.push(o), s.slice(0, p) + "$lit$" + s.slice(p) + e + y) : s + e + (-2 === p ? (l.push(void 0), i) : y);
        }
        const u = r + (t[o] || "<?>") + (2 === i ? "</svg>" : "");
        if (!Array.isArray(t) || !t.hasOwnProperty("raw")) throw Error("invalid template strings array");
        return [void 0 !== s ? s.createHTML(u) : u, l];
      };
    exports.render = x;
    exports.nothing = w;
    exports.noChange = b;
    exports.svg = y;
    exports.html = $;
    class E {
      constructor({
        strings: t,
        _$litType$: s
      }, n) {
        let l;
        this.parts = [];
        let r = 0,
          d = 0;
        const u = t.length - 1,
          c = this.parts,
          [v, a] = C(t, s);
        if (this.el = E.createElement(v, n), A.currentNode = this.el.content, 2 === s) {
          const t = this.el.content,
            i = t.firstChild;
          i.remove(), t.append(...i.childNodes);
        }
        for (; null !== (l = A.nextNode()) && c.length < u;) {
          if (1 === l.nodeType) {
            if (l.hasAttributes()) {
              const t = [];
              for (const i of l.getAttributeNames()) if (i.endsWith("$lit$") || i.startsWith(e)) {
                const s = a[d++];
                if (t.push(i), void 0 !== s) {
                  const t = l.getAttribute(s.toLowerCase() + "$lit$").split(e),
                    i = /([.?@])?(.*)/.exec(s);
                  c.push({
                    type: 1,
                    index: r,
                    name: i[2],
                    strings: t,
                    ctor: "." === i[1] ? M : "?" === i[1] ? H : "@" === i[1] ? I : S
                  });
                } else c.push({
                  type: 6,
                  index: r
                });
              }
              for (const i of t) l.removeAttribute(i);
            }
            if (g.test(l.tagName)) {
              const t = l.textContent.split(e),
                s = t.length - 1;
              if (s > 0) {
                l.textContent = i ? i.emptyScript : "";
                for (let i = 0; i < s; i++) l.append(t[i], h()), A.nextNode(), c.push({
                  type: 2,
                  index: ++r
                });
                l.append(t[s], h());
              }
            }
          } else if (8 === l.nodeType) if (l.data === o) c.push({
            type: 2,
            index: r
          });else {
            let t = -1;
            for (; -1 !== (t = l.data.indexOf(e, t + 1));) c.push({
              type: 7,
              index: r
            }), t += e.length - 1;
          }
          r++;
        }
      }
      static createElement(t, i) {
        const s = l.createElement("template");
        return s.innerHTML = t, s;
      }
    }
    function P(t, i, s = t, e) {
      var o, n, l, h;
      if (i === b) return i;
      let d = void 0 !== e ? null === (o = s._$Cl) || void 0 === o ? void 0 : o[e] : s._$Cu;
      const u = r(i) ? void 0 : i._$litDirective$;
      return (null == d ? void 0 : d.constructor) !== u && (null === (n = null == d ? void 0 : d._$AO) || void 0 === n || n.call(d, !1), void 0 === u ? d = void 0 : (d = new u(t), d._$AT(t, s, e)), void 0 !== e ? (null !== (l = (h = s)._$Cl) && void 0 !== l ? l : h._$Cl = [])[e] = d : s._$Cu = d), void 0 !== d && (i = P(t, d._$AS(t, i.values), d, e)), i;
    }
    class V {
      constructor(t, i) {
        this.v = [], this._$AN = void 0, this._$AD = t, this._$AM = i;
      }
      get parentNode() {
        return this._$AM.parentNode;
      }
      get _$AU() {
        return this._$AM._$AU;
      }
      p(t) {
        var i;
        const {
            el: {
              content: s
            },
            parts: e
          } = this._$AD,
          o = (null !== (i = null == t ? void 0 : t.creationScope) && void 0 !== i ? i : l).importNode(s, !0);
        A.currentNode = o;
        let n = A.nextNode(),
          h = 0,
          r = 0,
          d = e[0];
        for (; void 0 !== d;) {
          if (h === d.index) {
            let i;
            2 === d.type ? i = new N(n, n.nextSibling, this, t) : 1 === d.type ? i = new d.ctor(n, d.name, d.strings, this, t) : 6 === d.type && (i = new L(n, this, t)), this.v.push(i), d = e[++r];
          }
          h !== (null == d ? void 0 : d.index) && (n = A.nextNode(), h++);
        }
        return o;
      }
      m(t) {
        let i = 0;
        for (const s of this.v) void 0 !== s && (void 0 !== s.strings ? (s._$AI(t, s, i), i += s.strings.length - 2) : s._$AI(t[i])), i++;
      }
    }
    class N {
      constructor(t, i, s, e) {
        var o;
        this.type = 2, this._$AH = w, this._$AN = void 0, this._$AA = t, this._$AB = i, this._$AM = s, this.options = e, this._$Cg = null === (o = null == e ? void 0 : e.isConnected) || void 0 === o || o;
      }
      get _$AU() {
        var t, i;
        return null !== (i = null === (t = this._$AM) || void 0 === t ? void 0 : t._$AU) && void 0 !== i ? i : this._$Cg;
      }
      get parentNode() {
        let t = this._$AA.parentNode;
        const i = this._$AM;
        return void 0 !== i && 11 === t.nodeType && (t = i.parentNode), t;
      }
      get startNode() {
        return this._$AA;
      }
      get endNode() {
        return this._$AB;
      }
      _$AI(t, i = this) {
        t = P(this, t, i), r(t) ? t === w || null == t || "" === t ? (this._$AH !== w && this._$AR(), this._$AH = w) : t !== this._$AH && t !== b && this.$(t) : void 0 !== t._$litType$ ? this.T(t) : void 0 !== t.nodeType ? this.k(t) : u(t) ? this.S(t) : this.$(t);
      }
      M(t, i = this._$AB) {
        return this._$AA.parentNode.insertBefore(t, i);
      }
      k(t) {
        this._$AH !== t && (this._$AR(), this._$AH = this.M(t));
      }
      $(t) {
        this._$AH !== w && r(this._$AH) ? this._$AA.nextSibling.data = t : this.k(l.createTextNode(t)), this._$AH = t;
      }
      T(t) {
        var i;
        const {
            values: s,
            _$litType$: e
          } = t,
          o = "number" == typeof e ? this._$AC(t) : (void 0 === e.el && (e.el = E.createElement(e.h, this.options)), e);
        if ((null === (i = this._$AH) || void 0 === i ? void 0 : i._$AD) === o) this._$AH.m(s);else {
          const t = new V(o, this),
            i = t.p(this.options);
          t.m(s), this.k(i), this._$AH = t;
        }
      }
      _$AC(t) {
        let i = T.get(t.strings);
        return void 0 === i && T.set(t.strings, i = new E(t)), i;
      }
      S(t) {
        d(this._$AH) || (this._$AH = [], this._$AR());
        const i = this._$AH;
        let s,
          e = 0;
        for (const o of t) e === i.length ? i.push(s = new N(this.M(h()), this.M(h()), this, this.options)) : s = i[e], s._$AI(o), e++;
        e < i.length && (this._$AR(s && s._$AB.nextSibling, e), i.length = e);
      }
      _$AR(t = this._$AA.nextSibling, i) {
        var s;
        for (null === (s = this._$AP) || void 0 === s || s.call(this, !1, !0, i); t && t !== this._$AB;) {
          const i = t.nextSibling;
          t.remove(), t = i;
        }
      }
      setConnected(t) {
        var i;
        void 0 === this._$AM && (this._$Cg = t, null === (i = this._$AP) || void 0 === i || i.call(this, t));
      }
    }
    class S {
      constructor(t, i, s, e, o) {
        this.type = 1, this._$AH = w, this._$AN = void 0, this.element = t, this.name = i, this._$AM = e, this.options = o, s.length > 2 || "" !== s[0] || "" !== s[1] ? (this._$AH = Array(s.length - 1).fill(new String()), this.strings = s) : this._$AH = w;
      }
      get tagName() {
        return this.element.tagName;
      }
      get _$AU() {
        return this._$AM._$AU;
      }
      _$AI(t, i = this, s, e) {
        const o = this.strings;
        let n = !1;
        if (void 0 === o) t = P(this, t, i, 0), n = !r(t) || t !== this._$AH && t !== b, n && (this._$AH = t);else {
          const e = t;
          let l, h;
          for (t = o[0], l = 0; l < o.length - 1; l++) h = P(this, e[s + l], i, l), h === b && (h = this._$AH[l]), n || (n = !r(h) || h !== this._$AH[l]), h === w ? t = w : t !== w && (t += (null != h ? h : "") + o[l + 1]), this._$AH[l] = h;
        }
        n && !e && this.C(t);
      }
      C(t) {
        t === w ? this.element.removeAttribute(this.name) : this.element.setAttribute(this.name, null != t ? t : "");
      }
    }
    class M extends S {
      constructor() {
        super(...arguments), this.type = 3;
      }
      C(t) {
        this.element[this.name] = t === w ? void 0 : t;
      }
    }
    const k = i ? i.emptyScript : "";
    class H extends S {
      constructor() {
        super(...arguments), this.type = 4;
      }
      C(t) {
        t && t !== w ? this.element.setAttribute(this.name, k) : this.element.removeAttribute(this.name);
      }
    }
    class I extends S {
      constructor(t, i, s, e, o) {
        super(t, i, s, e, o), this.type = 5;
      }
      _$AI(t, i = this) {
        var s;
        if ((t = null !== (s = P(this, t, i, 0)) && void 0 !== s ? s : w) === b) return;
        const e = this._$AH,
          o = t === w && e !== w || t.capture !== e.capture || t.once !== e.once || t.passive !== e.passive,
          n = t !== w && (e === w || o);
        o && this.element.removeEventListener(this.name, this, e), n && this.element.addEventListener(this.name, this, t), this._$AH = t;
      }
      handleEvent(t) {
        var i, s;
        "function" == typeof this._$AH ? this._$AH.call(null !== (s = null === (i = this.options) || void 0 === i ? void 0 : i.host) && void 0 !== s ? s : this.element, t) : this._$AH.handleEvent(t);
      }
    }
    class L {
      constructor(t, i, s) {
        this.element = t, this.type = 6, this._$AN = void 0, this._$AM = i, this.options = s;
      }
      get _$AU() {
        return this._$AM._$AU;
      }
      _$AI(t) {
        P(this, t);
      }
    }
    const R = {
        L: "$lit$",
        P: e,
        V: o,
        I: 1,
        N: C,
        R: V,
        j: u,
        D: P,
        H: N,
        F: S,
        O: H,
        W: I,
        B: M,
        Z: L
      },
      z = window.litHtmlPolyfillSupport;
    exports._$LH = R;
    null == z || z(E, N), (null !== (t = globalThis.litHtmlVersions) && void 0 !== t ? t : globalThis.litHtmlVersions = []).push("2.2.6");
    
    },{}],32:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    var _customElement = require("@lit/reactive-element/decorators/custom-element.js");
    Object.keys(_customElement).forEach(function (key) {
      if (key === "default" || key === "__esModule") return;
      if (key in exports && exports[key] === _customElement[key]) return;
      Object.defineProperty(exports, key, {
        enumerable: true,
        get: function () {
          return _customElement[key];
        }
      });
    });
    var _property = require("@lit/reactive-element/decorators/property.js");
    Object.keys(_property).forEach(function (key) {
      if (key === "default" || key === "__esModule") return;
      if (key in exports && exports[key] === _property[key]) return;
      Object.defineProperty(exports, key, {
        enumerable: true,
        get: function () {
          return _property[key];
        }
      });
    });
    var _state = require("@lit/reactive-element/decorators/state.js");
    Object.keys(_state).forEach(function (key) {
      if (key === "default" || key === "__esModule") return;
      if (key in exports && exports[key] === _state[key]) return;
      Object.defineProperty(exports, key, {
        enumerable: true,
        get: function () {
          return _state[key];
        }
      });
    });
    var _eventOptions = require("@lit/reactive-element/decorators/event-options.js");
    Object.keys(_eventOptions).forEach(function (key) {
      if (key === "default" || key === "__esModule") return;
      if (key in exports && exports[key] === _eventOptions[key]) return;
      Object.defineProperty(exports, key, {
        enumerable: true,
        get: function () {
          return _eventOptions[key];
        }
      });
    });
    var _query = require("@lit/reactive-element/decorators/query.js");
    Object.keys(_query).forEach(function (key) {
      if (key === "default" || key === "__esModule") return;
      if (key in exports && exports[key] === _query[key]) return;
      Object.defineProperty(exports, key, {
        enumerable: true,
        get: function () {
          return _query[key];
        }
      });
    });
    var _queryAll = require("@lit/reactive-element/decorators/query-all.js");
    Object.keys(_queryAll).forEach(function (key) {
      if (key === "default" || key === "__esModule") return;
      if (key in exports && exports[key] === _queryAll[key]) return;
      Object.defineProperty(exports, key, {
        enumerable: true,
        get: function () {
          return _queryAll[key];
        }
      });
    });
    var _queryAsync = require("@lit/reactive-element/decorators/query-async.js");
    Object.keys(_queryAsync).forEach(function (key) {
      if (key === "default" || key === "__esModule") return;
      if (key in exports && exports[key] === _queryAsync[key]) return;
      Object.defineProperty(exports, key, {
        enumerable: true,
        get: function () {
          return _queryAsync[key];
        }
      });
    });
    var _queryAssignedElements = require("@lit/reactive-element/decorators/query-assigned-elements.js");
    Object.keys(_queryAssignedElements).forEach(function (key) {
      if (key === "default" || key === "__esModule") return;
      if (key in exports && exports[key] === _queryAssignedElements[key]) return;
      Object.defineProperty(exports, key, {
        enumerable: true,
        get: function () {
          return _queryAssignedElements[key];
        }
      });
    });
    var _queryAssignedNodes = require("@lit/reactive-element/decorators/query-assigned-nodes.js");
    Object.keys(_queryAssignedNodes).forEach(function (key) {
      if (key === "default" || key === "__esModule") return;
      if (key in exports && exports[key] === _queryAssignedNodes[key]) return;
      Object.defineProperty(exports, key, {
        enumerable: true,
        get: function () {
          return _queryAssignedNodes[key];
        }
      });
    });
    
    },{"@lit/reactive-element/decorators/custom-element.js":8,"@lit/reactive-element/decorators/event-options.js":9,"@lit/reactive-element/decorators/property.js":10,"@lit/reactive-element/decorators/query-all.js":11,"@lit/reactive-element/decorators/query-assigned-elements.js":12,"@lit/reactive-element/decorators/query-assigned-nodes.js":13,"@lit/reactive-element/decorators/query-async.js":14,"@lit/reactive-element/decorators/query.js":15,"@lit/reactive-element/decorators/state.js":16}],33:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    var _classMap = require("lit-html/directives/class-map.js");
    Object.keys(_classMap).forEach(function (key) {
      if (key === "default" || key === "__esModule") return;
      if (key in exports && exports[key] === _classMap[key]) return;
      Object.defineProperty(exports, key, {
        enumerable: true,
        get: function () {
          return _classMap[key];
        }
      });
    });
    
    },{"lit-html/directives/class-map.js":25}],34:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    var _join = require("lit-html/directives/join.js");
    Object.keys(_join).forEach(function (key) {
      if (key === "default" || key === "__esModule") return;
      if (key in exports && exports[key] === _join[key]) return;
      Object.defineProperty(exports, key, {
        enumerable: true,
        get: function () {
          return _join[key];
        }
      });
    });
    
    },{"lit-html/directives/join.js":26}],35:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    var _live = require("lit-html/directives/live.js");
    Object.keys(_live).forEach(function (key) {
      if (key === "default" || key === "__esModule") return;
      if (key in exports && exports[key] === _live[key]) return;
      Object.defineProperty(exports, key, {
        enumerable: true,
        get: function () {
          return _live[key];
        }
      });
    });
    
    },{"lit-html/directives/live.js":27}],36:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    var _ref = require("lit-html/directives/ref.js");
    Object.keys(_ref).forEach(function (key) {
      if (key === "default" || key === "__esModule") return;
      if (key in exports && exports[key] === _ref[key]) return;
      Object.defineProperty(exports, key, {
        enumerable: true,
        get: function () {
          return _ref[key];
        }
      });
    });
    
    },{"lit-html/directives/ref.js":28}],37:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    var _repeat = require("lit-html/directives/repeat.js");
    Object.keys(_repeat).forEach(function (key) {
      if (key === "default" || key === "__esModule") return;
      if (key in exports && exports[key] === _repeat[key]) return;
      Object.defineProperty(exports, key, {
        enumerable: true,
        get: function () {
          return _repeat[key];
        }
      });
    });
    
    },{"lit-html/directives/repeat.js":29}],38:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    var _unsafeHtml = require("lit-html/directives/unsafe-html.js");
    Object.keys(_unsafeHtml).forEach(function (key) {
      if (key === "default" || key === "__esModule") return;
      if (key in exports && exports[key] === _unsafeHtml[key]) return;
      Object.defineProperty(exports, key, {
        enumerable: true,
        get: function () {
          return _unsafeHtml[key];
        }
      });
    });
    
    },{"lit-html/directives/unsafe-html.js":30}],39:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    require("@lit/reactive-element");
    require("lit-html");
    var _litElement = require("lit-element/lit-element.js");
    Object.keys(_litElement).forEach(function (key) {
      if (key === "default" || key === "__esModule") return;
      if (key in exports && exports[key] === _litElement[key]) return;
      Object.defineProperty(exports, key, {
        enumerable: true,
        get: function () {
          return _litElement[key];
        }
      });
    });
    
    },{"@lit/reactive-element":17,"lit-element/lit-element.js":21,"lit-html":31}],40:[function(require,module,exports){
    "use strict";
    
    Object.defineProperty(exports, "__esModule", {
      value: true
    });
    exports.__assign = void 0;
    exports.__asyncDelegator = __asyncDelegator;
    exports.__asyncGenerator = __asyncGenerator;
    exports.__asyncValues = __asyncValues;
    exports.__await = __await;
    exports.__awaiter = __awaiter;
    exports.__classPrivateFieldGet = __classPrivateFieldGet;
    exports.__classPrivateFieldSet = __classPrivateFieldSet;
    exports.__createBinding = void 0;
    exports.__decorate = __decorate;
    exports.__exportStar = __exportStar;
    exports.__extends = __extends;
    exports.__generator = __generator;
    exports.__importDefault = __importDefault;
    exports.__importStar = __importStar;
    exports.__makeTemplateObject = __makeTemplateObject;
    exports.__metadata = __metadata;
    exports.__param = __param;
    exports.__read = __read;
    exports.__rest = __rest;
    exports.__spread = __spread;
    exports.__spreadArray = __spreadArray;
    exports.__spreadArrays = __spreadArrays;
    exports.__values = __values;
    /*! *****************************************************************************
    Copyright (c) Microsoft Corporation.
    
    Permission to use, copy, modify, and/or distribute this software for any
    purpose with or without fee is hereby granted.
    
    THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
    REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
    AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
    INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
    LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
    OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
    PERFORMANCE OF THIS SOFTWARE.
    ***************************************************************************** */
    /* global Reflect, Promise */
    
    var extendStatics = function (d, b) {
      extendStatics = Object.setPrototypeOf || {
        __proto__: []
      } instanceof Array && function (d, b) {
        d.__proto__ = b;
      } || function (d, b) {
        for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p];
      };
      return extendStatics(d, b);
    };
    function __extends(d, b) {
      if (typeof b !== "function" && b !== null) throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
      extendStatics(d, b);
      function __() {
        this.constructor = d;
      }
      d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    }
    var __assign = function () {
      exports.__assign = __assign = Object.assign || function __assign(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
          s = arguments[i];
          for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p)) t[p] = s[p];
        }
        return t;
      };
      return __assign.apply(this, arguments);
    };
    exports.__assign = __assign;
    function __rest(s, e) {
      var t = {};
      for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0) t[p] = s[p];
      if (s != null && typeof Object.getOwnPropertySymbols === "function") for (var i = 0, p = Object.getOwnPropertySymbols(s); i < p.length; i++) {
        if (e.indexOf(p[i]) < 0 && Object.prototype.propertyIsEnumerable.call(s, p[i])) t[p[i]] = s[p[i]];
      }
      return t;
    }
    function __decorate(decorators, target, key, desc) {
      var c = arguments.length,
        r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc,
        d;
      if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
      return c > 3 && r && Object.defineProperty(target, key, r), r;
    }
    function __param(paramIndex, decorator) {
      return function (target, key) {
        decorator(target, key, paramIndex);
      };
    }
    function __metadata(metadataKey, metadataValue) {
      if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(metadataKey, metadataValue);
    }
    function __awaiter(thisArg, _arguments, P, generator) {
      function adopt(value) {
        return value instanceof P ? value : new P(function (resolve) {
          resolve(value);
        });
      }
      return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) {
          try {
            step(generator.next(value));
          } catch (e) {
            reject(e);
          }
        }
        function rejected(value) {
          try {
            step(generator["throw"](value));
          } catch (e) {
            reject(e);
          }
        }
        function step(result) {
          result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected);
        }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
      });
    }
    function __generator(thisArg, body) {
      var _ = {
          label: 0,
          sent: function () {
            if (t[0] & 1) throw t[1];
            return t[1];
          },
          trys: [],
          ops: []
        },
        f,
        y,
        t,
        g;
      return g = {
        next: verb(0),
        "throw": verb(1),
        "return": verb(2)
      }, typeof Symbol === "function" && (g[Symbol.iterator] = function () {
        return this;
      }), g;
      function verb(n) {
        return function (v) {
          return step([n, v]);
        };
      }
      function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (_) try {
          if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
          if (y = 0, t) op = [op[0] & 2, t.value];
          switch (op[0]) {
            case 0:
            case 1:
              t = op;
              break;
            case 4:
              _.label++;
              return {
                value: op[1],
                done: false
              };
            case 5:
              _.label++;
              y = op[1];
              op = [0];
              continue;
            case 7:
              op = _.ops.pop();
              _.trys.pop();
              continue;
            default:
              if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) {
                _ = 0;
                continue;
              }
              if (op[0] === 3 && (!t || op[1] > t[0] && op[1] < t[3])) {
                _.label = op[1];
                break;
              }
              if (op[0] === 6 && _.label < t[1]) {
                _.label = t[1];
                t = op;
                break;
              }
              if (t && _.label < t[2]) {
                _.label = t[2];
                _.ops.push(op);
                break;
              }
              if (t[2]) _.ops.pop();
              _.trys.pop();
              continue;
          }
          op = body.call(thisArg, _);
        } catch (e) {
          op = [6, e];
          y = 0;
        } finally {
          f = t = 0;
        }
        if (op[0] & 5) throw op[1];
        return {
          value: op[0] ? op[1] : void 0,
          done: true
        };
      }
    }
    var __createBinding = Object.create ? function (o, m, k, k2) {
      if (k2 === undefined) k2 = k;
      Object.defineProperty(o, k2, {
        enumerable: true,
        get: function () {
          return m[k];
        }
      });
    } : function (o, m, k, k2) {
      if (k2 === undefined) k2 = k;
      o[k2] = m[k];
    };
    exports.__createBinding = __createBinding;
    function __exportStar(m, o) {
      for (var p in m) if (p !== "default" && !Object.prototype.hasOwnProperty.call(o, p)) __createBinding(o, m, p);
    }
    function __values(o) {
      var s = typeof Symbol === "function" && Symbol.iterator,
        m = s && o[s],
        i = 0;
      if (m) return m.call(o);
      if (o && typeof o.length === "number") return {
        next: function () {
          if (o && i >= o.length) o = void 0;
          return {
            value: o && o[i++],
            done: !o
          };
        }
      };
      throw new TypeError(s ? "Object is not iterable." : "Symbol.iterator is not defined.");
    }
    function __read(o, n) {
      var m = typeof Symbol === "function" && o[Symbol.iterator];
      if (!m) return o;
      var i = m.call(o),
        r,
        ar = [],
        e;
      try {
        while ((n === void 0 || n-- > 0) && !(r = i.next()).done) ar.push(r.value);
      } catch (error) {
        e = {
          error: error
        };
      } finally {
        try {
          if (r && !r.done && (m = i["return"])) m.call(i);
        } finally {
          if (e) throw e.error;
        }
      }
      return ar;
    }
    
    /** @deprecated */
    function __spread() {
      for (var ar = [], i = 0; i < arguments.length; i++) ar = ar.concat(__read(arguments[i]));
      return ar;
    }
    
    /** @deprecated */
    function __spreadArrays() {
      for (var s = 0, i = 0, il = arguments.length; i < il; i++) s += arguments[i].length;
      for (var r = Array(s), k = 0, i = 0; i < il; i++) for (var a = arguments[i], j = 0, jl = a.length; j < jl; j++, k++) r[k] = a[j];
      return r;
    }
    function __spreadArray(to, from, pack) {
      if (pack || arguments.length === 2) for (var i = 0, l = from.length, ar; i < l; i++) {
        if (ar || !(i in from)) {
          if (!ar) ar = Array.prototype.slice.call(from, 0, i);
          ar[i] = from[i];
        }
      }
      return to.concat(ar || Array.prototype.slice.call(from));
    }
    function __await(v) {
      return this instanceof __await ? (this.v = v, this) : new __await(v);
    }
    function __asyncGenerator(thisArg, _arguments, generator) {
      if (!Symbol.asyncIterator) throw new TypeError("Symbol.asyncIterator is not defined.");
      var g = generator.apply(thisArg, _arguments || []),
        i,
        q = [];
      return i = {}, verb("next"), verb("throw"), verb("return"), i[Symbol.asyncIterator] = function () {
        return this;
      }, i;
      function verb(n) {
        if (g[n]) i[n] = function (v) {
          return new Promise(function (a, b) {
            q.push([n, v, a, b]) > 1 || resume(n, v);
          });
        };
      }
      function resume(n, v) {
        try {
          step(g[n](v));
        } catch (e) {
          settle(q[0][3], e);
        }
      }
      function step(r) {
        r.value instanceof __await ? Promise.resolve(r.value.v).then(fulfill, reject) : settle(q[0][2], r);
      }
      function fulfill(value) {
        resume("next", value);
      }
      function reject(value) {
        resume("throw", value);
      }
      function settle(f, v) {
        if (f(v), q.shift(), q.length) resume(q[0][0], q[0][1]);
      }
    }
    function __asyncDelegator(o) {
      var i, p;
      return i = {}, verb("next"), verb("throw", function (e) {
        throw e;
      }), verb("return"), i[Symbol.iterator] = function () {
        return this;
      }, i;
      function verb(n, f) {
        i[n] = o[n] ? function (v) {
          return (p = !p) ? {
            value: __await(o[n](v)),
            done: n === "return"
          } : f ? f(v) : v;
        } : f;
      }
    }
    function __asyncValues(o) {
      if (!Symbol.asyncIterator) throw new TypeError("Symbol.asyncIterator is not defined.");
      var m = o[Symbol.asyncIterator],
        i;
      return m ? m.call(o) : (o = typeof __values === "function" ? __values(o) : o[Symbol.iterator](), i = {}, verb("next"), verb("throw"), verb("return"), i[Symbol.asyncIterator] = function () {
        return this;
      }, i);
      function verb(n) {
        i[n] = o[n] && function (v) {
          return new Promise(function (resolve, reject) {
            v = o[n](v), settle(resolve, reject, v.done, v.value);
          });
        };
      }
      function settle(resolve, reject, d, v) {
        Promise.resolve(v).then(function (v) {
          resolve({
            value: v,
            done: d
          });
        }, reject);
      }
    }
    function __makeTemplateObject(cooked, raw) {
      if (Object.defineProperty) {
        Object.defineProperty(cooked, "raw", {
          value: raw
        });
      } else {
        cooked.raw = raw;
      }
      return cooked;
    }
    ;
    var __setModuleDefault = Object.create ? function (o, v) {
      Object.defineProperty(o, "default", {
        enumerable: true,
        value: v
      });
    } : function (o, v) {
      o["default"] = v;
    };
    function __importStar(mod) {
      if (mod && mod.__esModule) return mod;
      var result = {};
      if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
      __setModuleDefault(result, mod);
      return result;
    }
    function __importDefault(mod) {
      return mod && mod.__esModule ? mod : {
        default: mod
      };
    }
    function __classPrivateFieldGet(receiver, state, kind, f) {
      if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a getter");
      if (typeof state === "function" ? receiver !== state || !f : !state.has(receiver)) throw new TypeError("Cannot read private member from an object whose class did not declare it");
      return kind === "m" ? f : kind === "a" ? f.call(receiver) : f ? f.value : state.get(receiver);
    }
    function __classPrivateFieldSet(receiver, state, value, kind, f) {
      if (kind === "m") throw new TypeError("Private method is not writable");
      if (kind === "a" && !f) throw new TypeError("Private accessor was defined without a setter");
      if (typeof state === "function" ? receiver !== state || !f : !state.has(receiver)) throw new TypeError("Cannot write private member to an object whose class did not declare it");
      return kind === "a" ? f.call(receiver, value) : f ? f.value = value : state.set(receiver, value), value;
    }
    
    },{}]},{},[5]);
    