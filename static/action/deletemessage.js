export default function deleteMessage(index){
	return{
		type:'MESSAGE_REMOVE',
		index
	};
}
