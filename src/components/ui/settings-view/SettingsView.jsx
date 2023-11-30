import { useState } from 'react';
import styles from './SettingsView.module.scss';
const SettingsView = () => {
	const [position, setPosition] = useState(0);

	const handleMouseDown = e => {
		document.addEventListener('mousemove', handleMouseMove);
		document.addEventListener('mouseup', handleMouseUp);
	};

	const handleMouseMove = e => {
		// Рассчитываем новую позицию ползунка в зависимости от движения мыши
		const newPosition = e.clientX;
		setPosition(newPosition);
	};

	const handleMouseUp = () => {
		// Удаляем слушателей событий при отпускании мыши
		document.removeEventListener('mousemove', handleMouseMove);
		document.removeEventListener('mouseup', handleMouseUp);
	};

	return (
		<div className={styles.slider}>
			<div
				className={styles.thumb}
				style={{ left: `${position}px` }}
				onMouseDown={handleMouseDown}
			/>
		</div>
	);
};

export default SettingsView;
