let initialState = { messages:[]};
const messages = (state = initialState, action) => {
    switch (action.type) {
        case 'MESSAGE_ADD':{
            return {messages: [...state.messages, action.messages]}
        };
        case 'MESSAGE_REMOVE': {
            return {messages: [...state.messages.filter((message, item) =>  item!==action.index)]}
        };
        case 'MESSGE_UPDATE': {
            return state;
        };
        case 'REWRITE_MESSAGES':{
            return {messages: [...action.messages]}
        };
        default:
            return state;
    };
};

export default messages;
