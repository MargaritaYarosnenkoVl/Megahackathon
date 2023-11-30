import { Link } from 'react-router-dom';
import styles from './NavigateBar.module.scss';

const NavigateBar = ({ location }) => {
	return (
		<div className={styles.wrapper}>
			<Link to={'/home'}>Главная</Link>
			<p>/</p>
			{location !== 'later' ? (
				<Link to={'/home/laterRead'}>Читать потом</Link>
			) : (
				<p>Читать потом</p>
			)}
			<p>/</p>
			{location !== 'favorite' ? (
				<Link to={'/home/favorite'}>Избранное</Link>
			) : (
				<p>Избранное</p>
			)}
			<p>/</p>
			{location !== 'folders' ? (
				<Link to={'/home/folders'}>Мои папки</Link>
			) : (
				<p>Мои папки</p>
			)}
			<p>/</p>
			{location !== 'history' ? (
				<Link to={'/home/history'}>История просмотра</Link>
			) : (
				<p>История просмотра</p>
			)}
		</div>
	);
};

export default NavigateBar;
