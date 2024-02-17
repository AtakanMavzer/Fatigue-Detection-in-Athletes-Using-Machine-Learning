import React from 'react';
import JSCharting from 'jscharting-react';
import { useSelector } from 'react-redux';
import { computePlayerdata, computeTotalData } from './Compute';

  
const divStyle = {
	maxWidth: '780px',
	height: '260px',
	margin: '0px auto'
};
//

export default function Example(props) {
	const {isSuccess} = useSelector((state) => state.dataPlayer);
	const { data } = useSelector((state) => state.data)
  	const { dataPlayer } = useSelector((state) => state.dataPlayer)
	
	if( !isSuccess){
		return <div>Please Select a Player</div>
	//
	}else{
		
		const {type} = props
		let new_data;
		let config = {
			type: 'calendar months solid',
			data: [],
			legend: { title_label_text: 'Select a month', title_label_font_size: '12px' },
			defaultPoint: {
				label: { verticalAlign: 'top', padding: 3 },
				tooltip: '<b>{%date:date D}</b><br> Fatigue Value: {%zValue}'
			},
			palette_colorBar_axis_scale_interval: 100,
			toolbar_visible: false
		};
		
		if (type==='dataPlayer'){
			new_data=computePlayerdata(dataPlayer)
		}else if(type==='totalData'){
			new_data=computeTotalData(data)
			
		}
		config.data=new_data
		
		return (
			<div style={divStyle}>
				<JSCharting options={config} />
			</div>
		);
	}
	
}
