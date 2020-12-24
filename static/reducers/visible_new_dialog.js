let initialState = { visible_new_dialog: false };
const dialogs = (state = initialState, action) => {
  switch (action.type) {
    case 'UPDATE_VISIBLE_NEW_DIALOG':{
      return {visible_new_dialog: action.visible_new_dialog}
    };
    default:
      return state;
  };
};

export default dialogs;
