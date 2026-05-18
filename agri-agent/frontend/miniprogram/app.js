// app.js
App({
  onLaunch() {
    if (wx.cloud) {
      wx.cloud.init({
        env: '', // 替换成上一步复制的环境ID
        traceUser: true,
      });
    }
    console.log('农信智盾启动');
  }
});