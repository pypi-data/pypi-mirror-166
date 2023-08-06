import { c as configureLocalization, s, i, y, u as updateWhenLocaleChanges, a as setCookie, m as msg, b as cleanPath, t as tc_shares, d as tc_filelist, e as tc_fileupload } from './filelist-6e4e6322.js';

const supportedLocales = ["en", "zh-CN"];
const {
  getLocale,
  setLocale
} = configureLocalization({
  sourceLocale: "en",
  targetLocales: supportedLocales,
  loadLocale: locale => import(`/static/locale/${locale}.js`)
});
const decideLocale = localeName => {
  if (supportedLocales.includes(localeName)) {
    return localeName;
  }

  if (localeName.startsWith("en")) {
    return "en";
  }

  if (localeName.startsWith("zh")) {
    return "zh-CN";
  }

  return undefined;
};

class tc_settings extends s {
  static properties = {
    content: {}
  };
  static styles = i`pre{margin:0}`;

  constructor() {
    super();
    this.token = localStorage["token"];
  }

  loadData() {
    fetch("/api/confmgr").then(resp => {
      resp.json().then(res => {
        this.content = res;
      });
    });
  }

  save() {
    var items = this.shadowRoot.querySelectorAll("input"); //.configItem");

    for (var i of items.keys()) {
      var path = items[i].getAttribute("tc-config-tree").split("-");
      var value = items[i].value;
      var orig = this.content;

      for (var n in path.slice(0, -1)) {
        orig = orig[path[n]];
      }

      orig[path.slice(-1)] = value;
    }
  }

  render() {
    if (this.content) {
      var h = [];

      var genHtml = (obj, lavel, name) => {
        if (typeof obj != "object") {
          return y`<input class="configItem" tc-config-tree="${name.slice(1)}" value="${obj}">`;
        }

        var ret = [];

        for (var i in obj) {
          ret.push(y`<pre>${"  ".repeat(lavel)} ${i}:${genHtml(obj[i], lavel + 1, [name, i].join("-"))}<pre></pre></pre>`);
        } //          ret.push(html`<pre>${"   ".repeat(lavel)}<button>New</button><pre>`)


        return ret;
      };

      h = genHtml(this.content, 0, "");
      return y`${h}<button>Summit</button>`;
    }
  }

}
customElements.define("tc-settings", tc_settings);

class tc_login extends s {
  static properties = {};

  constructor() {
    super();
    updateWhenLocaleChanges(this);
  }

  login() {
    setCookie("token", "", 0);
    var username = this.shadowRoot.getElementById("username").value;
    var passwd = this.shadowRoot.getElementById("passwd").value;
    fetch("/api/auth/login", {
      method: "POST",
      headers: {
        Authorization: "Basic " + btoa(username + ":" + passwd)
      }
    }).then(res => {
      res.json().then(res => {
        if (res.status == 200) {
          localStorage.token = res.token;
          window.tinycloud.needLogin = false;
          window.tinycloud.update();
        }
      });
    });
  }

  render() {
    return y`<center><label for="username">${msg("Username")}:</label><input tyep="text" id="username"><br><label for="passwd">${msg("Password")}:</label><input type="password" id="passwd"><br><button @click="${this.login}">${msg("Login")}</button></center>`;
  }

}
customElements.define("tc-login", tc_login);

class tinycloud extends s {
  static properties = {
    url: {},
    routes: {}
  };
  static styles = i`a{color:var(--tc-link-color,#00f)}`;

  constructor() {
    super();
    window.tinycloud = this;
    window.setLocale = setLocale;
    var browserLang = navigator.language;
    updateWhenLocaleChanges(this);
    setLocale(decideLocale(browserLang) || en).then(() => {
      this.localeOk = true;
      this.update();
    });

    if (location.hash.split("#")[1]) {
      this.url = cleanPath(location.hash.split("#")[1]);
    } else {
      this.url = "/";
    }

    window.addEventListener("hashchange", () => {
      this.hashchange();
    }, false);
    this.routes = {
      files: [this.contentFiles, () => msg("Files")],
      settings: [this.contentSettings, () => msg("Settings")],
      shares: [this.contentShares, () => msg("Shares")],
      logout: [() => {
        delete localStorage["token"];
        location.hash = "files";
        this.update();
      }, () => msg("Logout")]
    };
  }

  hashchange() {
    this.url = cleanPath(location.hash.split("#")[1]);
  }

  contentSettings = () => {
    var settings = new tc_settings();
    settings.loadData();
    return y`${settings}`;
  };
  contentShares = () => {
    var shares = new tc_shares();
    shares.loadData();
    return y`${shares}`;
  };
  contentFiles = () => {
    var url = "/" + this.url.split("/").slice(2).join("/");
    var urlRoot = this.url.split("/").slice(0, 2).join("/");
    var filelist = new tc_filelist();
    filelist.url = url;
    filelist.urlRoot = urlRoot;
    var fileupload = new tc_fileupload();
    fileupload.url = url;
    fileupload.uploadFinishedCallback = filelist.uploadFinishedCallback;
    fileupload.uploadProgressCallback = filelist.uploadProgressCallback;
    filelist.file_upload = fileupload;
    filelist.loadData();
    return y`${filelist}${fileupload}`;
  }; // Render the UI as a function of component state

  render() {
    //console.log(this.url.split('/')[])
    if (!this.localeOk) {
      return;
    }

    if (this.needLogin == undefined && localStorage["token"]) {
      fetch("/api/auth/check", {
        method: "POST",
        header: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          token: localStorage["token"]
        })
      }).then(res => {
        res.json().then(res => {
          console.log(2);
          this.needLogin = res.status != 200;
          this.update();
        });
      });
      return;
    }

    if (!localStorage["token"]) {
      console.log(1);
      this.needLogin = true;
    }

    if (this.needLogin) {
      var login = true;

      var contFunc = () => {
        return new tc_login();
      };
    }

    var menu = [];

    if (!login) {
      setCookie("token", localStorage["token"]);

      if (this.url == "/") {
        location.hash = "/files";
      }

      for (var i in this.routes) {
        menu.push([this.routes[i][1], this.routes[i][0], i]);
      }

      var contFunc = this.routes[this.url.split("/")[1]][0];
    }

    return y`<body><div id="header">Tinycloud0.1<div align="right">${menu.map(x => y`<a href="#${x[2]}">${x[0]()}</a> `)}</div><hr></div><div id="content">${contFunc()}</div></body>`;
  }

}
customElements.define("tc-main", tinycloud);

export { tinycloud };
