export default function rewriteMessages(messages){
	return{
		type:'REWRITE_MESSAGES',
		messages
	};
}