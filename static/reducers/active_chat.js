let initialState = { active_chat:''};
const active_chat = (state = initialState, action) => {
  switch (action.type) {
    case 'CHANGE_ACTIVE_CHAT':{
      return {active_chat: action.chat_id}
    };
    default:
      return state;
  };
};

export default active_chat;
