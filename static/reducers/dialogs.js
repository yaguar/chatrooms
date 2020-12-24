let initialState = { dialogs:[]};
const dialogs = (state = initialState, action) => {
  switch (action.type) {
    case 'REWRITE_DIALOGS':{
      return {dialogs: [...action.dialogs]}
    };
    default:
      return state;
  };
};

export default dialogs;
