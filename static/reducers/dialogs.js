let initialState = { dialogs:[]};
const dialogs = (state = initialState, action) => {
  switch (action.type) {
    case 'NEW_DIALOG': {
      return {dialogs: [action.dialog, ...state.dialogs]}
    }
    case 'REWRITE_DIALOGS':{
      return {dialogs: [...action.dialogs]}
    };
    case 'ZERO_UNREAD_MSG': {
      return {dialogs: [...state.dialogs.map((dlg, index) =>  { if (dlg.id==action.chat_id) {dlg.unread=0} return dlg})]}
    };
    case 'ADD_UNREAD_MSG': {
      return {dialogs: [...state.dialogs.map((dlg, index) =>  { if (dlg.id==action.chat_id) {dlg.unread+=1} return dlg})]}
    };
    case 'UP_DIALOG': {
      let obj = state.dialogs.filter(function(dlg) {
          return dlg.id==action.message.chat_id
      });
      obj[0].msg = action.message.msg
      return {dialogs: [obj[0], ...state.dialogs.filter(function(dlg) {return dlg.id!=action.message.chat_id})]}
    }
    default:
      return state;
  };
};

export default dialogs;
