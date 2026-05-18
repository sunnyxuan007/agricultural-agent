// utils/api.js
const BASE_URL = 'https://';   // 模拟器可直接访问 localhost，实际真机用IP地址或ngrok网络刺穿，这里需要填写

function ask(question) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: BASE_URL + '/chat',
      method: 'POST',
      data: { message: question },
      success(res) {
        if (res.data && res.data.answer) {
          resolve(res.data.answer);
        } else {
          reject(new Error('返回数据格式错误'));
        }
      },
      fail(err) {
        reject(err);
      }
    });
  });
}

module.exports = { ask };