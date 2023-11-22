import Header from '../../header/Header';
import InsideInfo from '../../inside-info/InsideInfo';
import LeftPanel from '../../left-panel/LeftPanel';
import styles from './PersonalArea.module.scss';

const PersonalArea = () => {
	return (
		<div className={styles.wrapper}>
			<Header />
			<div className={styles.block_content}>
				<LeftPanel />
				<InsideInfo />
			</div>
		</div>
	);
};

export default PersonalArea;
