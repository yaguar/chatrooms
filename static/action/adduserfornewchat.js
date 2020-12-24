export default function addUserForNewChat(users_for_new_chat){
	return{
		type:'USERS_FOR_NEW_CHAT_ADD',
		users_for_new_chat
	};
}