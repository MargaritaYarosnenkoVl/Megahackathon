import { useState } from 'react';
import styles from './Checkbox.module.scss';

const Checkbox = ({ children, id, register }) => {
	const [test, setTest] = useState(false);

	return (
		<div className={styles.checkbox}>
			<img
				src={
					test
						? './images/icons/checkbox_on.svg'
						: './images/icons/checkbox_off.svg'
				}
				alt='image'
			/>
			<input
				{...register(`${id}`)}
				id={id}
				type='checkbox'
				onClick={() => setTest(!test)}
			/>
			<label htmlFor={id}>{children}</label>
		</div>
	);
};

export default Checkbox;
