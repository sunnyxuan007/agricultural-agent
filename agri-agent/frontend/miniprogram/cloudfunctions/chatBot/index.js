const cloud = require('wx-server-sdk');
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV });

exports.main = async (event) => {
  // ========== 添加调试日志 ==========
  console.log('收到消息:', event.message);
  console.log('当前环境ID:', cloud.getWXContext().ENV);
  console.log('云函数调用开始');
  // =================================

  try {
    const res = await cloud.openapi.tcb.ai.chatCompletions({
      model: 'hunyuan-turbos-latest',
      messages: [
        { role: 'system', content: '你是农业金融助手，回答农户问题。' },
        { role: 'user', content: event.message }
      ]
    });
    const answer = res.choices?.[0]?.message?.content || '抱歉，我无法回答。';
    console.log('调用成功，回答：', answer);
    return { code: 0, data: { response: answer } };
  } catch (err) {
    console.error('云函数错误:', err);
    return { code: -1, message: err.message };
  }
};