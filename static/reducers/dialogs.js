let initialState = { dialogs:[]};
const dialogs = (state = initialState, action) => {
  switch (action.type) {
    case 'REWRITE_DIALOGS':{
      return {dialogs: [...action.dialogs]}
    };
    case 'ZERO_UNREAD_MSG': {
      return {dialogs: [...state.dialogs.map((dlg, index) =>  { if (dlg.id==action.chat_id) {dlg.unread=0} return dlg})]}
    }
    default:
      return state;
  };
};

export default dialogs;
