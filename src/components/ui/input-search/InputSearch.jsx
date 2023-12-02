import { useFilter } from '../../../hooks/useFilter';
import useSearchNews from '../../../hooks/useSearchNews';
import { FilterContext } from '../../../providers/FilterProvider';
import styles from './InputSearch.module.scss';

const InputSearch = ({ filter }) => {
	const { setIsViewFilter } = useFilter(FilterContext);

	const { result, request, stop_parse } = useSearchNews();

	return (
		<div className={styles.block__header_settings}>
			{filter === 'yes' && (
				<button
					className={styles.button__filtr}
					onClick={() => setIsViewFilter(true)}
				>
					<img src='../images/icons/filtr.svg' alt='img' />
					Фильтры
				</button>
			)}
			<div className={styles.block__search}>
				<img
					className={styles.search__image}
					src='../images/icons/search.svg'
					alt='search'
				/>
				<input className={styles.search} type='text' placeholder='Поиск' />
			</div>
			<button className={styles.image__pars} onClick={stop_parse}>
				<img src='../images/icons/stop_pars_white.svg' alt='stop' />
			</button>
			<button className={styles.image__pars} onClick={result}>
				<img src='../images/icons/reload_white.svg' alt='reload' />
			</button>
		</div>
	);
};

export default InputSearch;
