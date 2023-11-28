import styles from './TitleList.module.scss';

const TitleList = () => {
	return (
		<div className={styles.block__titles}>
			<h2>Источник</h2>
			<h2>Новость</h2>
			<h2>Редактирование</h2>
			<h2>Теги</h2>
		</div>
	);
};

export default TitleList;
