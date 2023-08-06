import { s, b as cleanPath, d as tc_filelist, y } from './filelist-6e4e6322.js';

class tc_share extends s {
  static properties = {
    id: {},
    url: {},
    fullUrl: {},
    info: {}
  };

  constructor() {
    super();

    window.onhashchange = () => {
      this.loadData();
    };

    this.fullUrl = location.pathname.split("/shares/")[1];
    this.id = this.fullUrl.split("/")[0];
    this.loadData();
  }

  loadData() {
    this.url = cleanPath(this.fullUrl.split("/").slice(1).join("/") + "/" + location.hash.slice(1));
    fetch("/api/shares/info/" + this.id).then(res => {
      res.json().then(res => {
        this.info = res;
      });
    });
  }

  render() {
    if (!this.info) {
      return;
    }

    var filelist = new tc_filelist();
    filelist.readOnly = this.info.mode == "r";
    filelist.apiBase = "/api/shares/dav/" + this.id;
    filelist.url = "/" + this.url;
    filelist.loadData();
    return y`${filelist}`;
  }

}
customElements.define("tc-share", tc_share);

export { tc_share };
