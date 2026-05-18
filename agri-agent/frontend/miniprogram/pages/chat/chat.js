const api = require('../../utils/api.js');

Page({
  data: {
    activeTab: 'chat',
    inputValue: '',
    messages: [],
    currentAgent: null,
    isLoading: false,
    showFeatureCards: true
  },

  onLoad() {
    this.addMessage('ai', '您好！我是农信智盾，可以问贷款、补贴、农技问题。');
  },

  switchTab(e) {
    this.setData({ activeTab: e.currentTarget.dataset.tab });
  },

  onInput(e) {
    this.setData({ inputValue: e.detail.value });
  },

  onVoice() {
    wx.showToast({ title: '语音功能开发中', icon: 'none' });
  },

  onPlus() {
    wx.showActionSheet({
      itemList: ['发送图片', '发送文件', '语音通话'],
      success: (res) => console.log('选择了：', res.tapIndex)
    });
  },

  onSend() {
    if (this.data.inputValue && this.data.inputValue.trim()) {
      this.sendMessage(this.data.inputValue);
    }
  },

  onQuickTagTap(e) {
    const tag = e.currentTarget.dataset.tag;
    let query = '';
    switch (tag) {
      case 'weather': query = '今天天气怎么样？适合进行农事活动吗？'; break;
      case 'product-recommend': query = '有什么优质的农资产品推荐？'; break;
      case 'price-trend': query = '最近农产品价格走势如何？'; break;
      case 'loan-consult': query = '我想了解一下贷款产品'; break;
    }
    this.setData({ inputValue: query });
    this.sendMessage(query);
  },

  toggleFeatureCards() {
    this.setData({ showFeatureCards: !this.data.showFeatureCards });
  },

  onFeatureTap(e) {
    const feature = e.currentTarget.dataset.feature;
    let query = '';
    switch (feature) {
      case 'price-trend': query = '帮我预测一下近期的农产品价格走势'; break;
      case 'market-info': query = '有哪些优质的农资供应商？'; break;
      case 'planting-plan': query = '我想规划一下种植方案'; break;
      case 'content-analysis': query = '分析一下当前的农产品市场'; break;
    }
    this.setData({ inputValue: query });
    this.sendMessage(query);
  },

  onCamera() {
    wx.chooseMedia({
      count: 1, mediaType: ['image'], sourceType: ['camera'],
      success: () => wx.showToast({ title: '图片已选择', icon: 'success' })
    });
  },

  onUploadImage() {
    wx.chooseMedia({
      count: 1, mediaType: ['image'], sourceType: ['album'],
      success: () => wx.showToast({ title: '图片已选择', icon: 'success' })
    });
  },

  onUploadFile() {
    wx.chooseMessageFile({
      count: 1, type: 'file',
      success: () => wx.showToast({ title: '文件已选择', icon: 'success' })
    });
  },

  onCall() {
    wx.makePhoneCall({ phoneNumber: '95588', fail: () => wx.showToast({ title: '拨号失败', icon: 'none' }) });
  },

  onSettings() {
    wx.showToast({ title: '设置功能开发中', icon: 'none' });
  },

  onAgentTap(e) {
    const agent = e.currentTarget.dataset.agent;
    const agentNames = {
      'sales': '销售决策助手', 'finance': '融资管理助手', 'risk': '风险预警助手',
      'planting': '种植规划助手', 'policy': '政策资讯助手', 'service': '智能客服'
    };
    this.setData({ currentAgent: agent, activeTab: 'chat' });
    wx.showToast({ title: `已选择${agentNames[agent]}`, icon: 'success' });

    const welcomeMessages = {
      'sales': '我是销售决策助手，可以帮您分析市场行情、预测价格走势、推荐最佳销售时机。请问您种植的是什么作物？',
      'finance': '我是融资管理助手，可以帮您匹配合适的贷款产品、制定还款计划。请问您需要多少额度的贷款？',
      'risk': '我是风险预警助手，可以为您提供天气预警、价格波动提醒等服务。请问您最关心哪方面的风险？',
      'planting': '我是种植规划助手，可以帮您选择作物品种、测算种植规模。请问您的土地面积和所在地区是？',
      'policy': '我是政策资讯助手，可以为您提供最新的农业补贴政策、行业动态。请问您想了解哪方面的政策？',
      'service': '我是智能客服，7×24小时为您服务。请问有什么可以帮您的？'
    };
    setTimeout(() => this.addMessage('ai', welcomeMessages[agent]), 300);
  },

  sendMessage(message) {
    if (!message || !message.trim()) return;

    this.addMessage('user', message);
    this.setData({ 
      inputValue: '', 
      isLoading: true,
      showFeatureCards: false
    });
    wx.showLoading({ title: 'AI思考中...', mask: true });

    api.ask(message)
      .then(answer => {
        wx.hideLoading();
        this.setData({ isLoading: false });
        this.addMessage('ai', answer);
      })
      .catch(err => {
        wx.hideLoading();
        this.setData({ isLoading: false });
        console.error('请求失败:', err);
        let fallbackAnswer = '网络连接失败，请检查后端是否启动，或 IP 地址是否正确。';
        this.addMessage('ai', fallbackAnswer);
      });
  },

  addMessage(type, content) {
    const messages = this.data.messages;
    messages.push({ type, content, time: this.getCurrentTime() });
    this.setData({ messages });
  },

  getCurrentTime() {
    const now = new Date();
    return `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
  }
});