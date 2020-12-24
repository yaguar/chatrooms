let initialState = { maybe_users_for_new_chat:[]};
const maybe_users_for_new_chat = (state = initialState, action) => {
    switch (action.type) {
        case 'REWRITE_MAYBE_USERS_FOR_NEW_CHAT':{
            return {maybe_users_for_new_chat: [...action.users]}
        };
        default:
            return state;
    };
};

export default maybe_users_for_new_chat;
