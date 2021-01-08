import React from 'react';
import SearchField from "react-search-field";
import updateVisibleNewDialog from "../action/updatevisiblenewdialog";

const DivSearchField = (props) => {

    const onChange = (value) => {
        let body = JSON.stringify({
                type: 'GET_CHATS',
                search: value
        })
        props.websocket.send(body)
    }

    // const updateVND = (visible) => {dispatch(updateVisibleNewDialog(visible))}

    return (
        <div>
            <SearchField
                placeholder="Search..."
                onChange={onChange}
            />&nbsp;&nbsp;<span><i className="fa fa-plus-square-o fa-lg" onClick={()=>props.updateVND(true)}/></span>
        </div>
    );
}

export default DivSearchField;