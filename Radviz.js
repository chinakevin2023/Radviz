function Radviz(c) {
  let config = {
    ID: {},
    data: [],
    canvas: {},
    xo: 500,
    yo: 400,
    r: 300,
    width: 1000,
    height: 800,
  };

  this.get = function (key) {
    return config[key];
  };

  this.set = function (key, val) {
    config[key] = val;
  };

  this.norm = function (key, data) {
    // let low = Number(data[0][key]),
    //   high = Number(data[0][key]);
    // for (let i = 1; i < data.length; i++) {
    //   low = Math.min(low, Number(data[i][key]));
    //   high = Math.max(high, Number(data[i][key]));
    // }
    // for (let i = 0; i < data.length; i++) {
    //   data[i][key] = (Number(data[i][key]) - low) / (high - low);
    // }
    for (let i = 0; i < data.length; i++) {
      data[i][key] = Number(data[i][key]);
    }
  };

  this.draw = function (subs) {
    let data = this.get("data");
    let canvas = this.get("canvas");
    let ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    let xo = this.get("xo"),
      yo = this.get("yo"),
      r = this.get("r");
    let keys = [];
    for (let key of subs) {
      // data[0]
      if (key == "id" || key == "className" || key == "classId") continue;
      keys.push(key);
      this.norm(key, data);
    }
    console.log(keys);
    // subs = [keys[4], keys[3], keys[5], keys[1], keys[2], keys[0]];
    // keys = subs;
    // console.log(subs);
    // let keys2 = keys.slice(0);
    // for (let i = 0; i < subs.length; i++) keys[i] = keys2[subs[i]];
    // console.log(keys);
    let n = keys.length;
    // let n = 4;
    let color = [
      "red",
      "green",
      "blue",
      "purple",
      "orange",
      "pink",
      "gray",
      "yellow",
    ];
    ctx.stroke();
    let rd = 5;
    for (let i = 0; i < n; i++) {
      ctx.lineWidth = 30;
      ctx.strokeStyle = color[i];
      ctx.beginPath();
      ctx.arc(
        xo,
        yo,
        r,
        ((Math.PI * 2) / n) * i,
        ((Math.PI * 2) / n) * (i + 1),
        false
      );
      ctx.stroke();
      let x = xo + r * Math.cos((2 * Math.PI * (2 * i + 1)) / 2 / n);
      let y = yo + r * Math.sin((2 * Math.PI * (2 * i + 1)) / 2 / n);
      ctx.lineWidth = 5;
      ctx.fillStyle = "white";
      ctx.beginPath();
      ctx.arc(x, y, rd, 0, 2 * Math.PI, false);
      ctx.fill();
      ctx.fillStyle = "black";
      ctx.font = "normal 20px Arial";
      ctx.fillText(keys[i], x, y);
    }
    for (let i = 0; i < data.length; i++) {
      let s0 = 0,
        s1 = 0,
        s2 = 0;
      for (let j = 0; j < keys.length; j++) {
        // if (i == 1) console.log(i, " ", data[i][keys[j]]);
        s0 += data[i][keys[j]] * (r * Math.cos((2 * Math.PI * j) / n));
        s1 += data[i][keys[j]] * (r * Math.sin((2 * Math.PI * j) / n));
        s2 += data[i][keys[j]];
      }
      let x = s2 == 0 ? xo : xo + s0 / s2;
      let y = s2 == 0 ? yo : yo + s1 / s2;
      ctx.beginPath();
      ctx.arc(x, y, 5, 0, 2 * Math.PI, true);
      //   ctx.fillStyle = data[i]["color"];
      console.log(data[i]["classId"]);
      ctx.fillStyle = color[Number(data[i]["classId"])];
      ctx.fill();
      //   ctx.fillText(data[i]["id"], x, y);
    }
  };

  this.init = function (subs) {
    this.set("ID", c["ID"]);
    this.set("data", c["data"]);
    let canvas = document.createElement("canvas");
    this.set("canvas", canvas);
    (canvas.width = 1000), (canvas.height = 800);
    let id = this.get("ID");
    let element = document.getElementById(id);
    console.log(element);
    let width = element.offsetWidth,
      height = element.offsetHeight;
    this.set("width", width), this.set("height", height);
    element.appendChild(canvas);
    this.draw(subs);
  };
}
