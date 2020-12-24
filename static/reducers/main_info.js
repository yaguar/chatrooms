let initialState = { main_info:{}};
const main_info = (state = initialState, action) => {
  switch (action.type) {
    case 'ADD_MAIN_INFO':{
      return {main_info: {'id': action.main_info.id, 'login': action.main_info.login}}
    };
    default:
      return state;
  };
};

export default main_info;