import { useFilter } from '../../hooks/useFilter';
import useSearchNews from '../../hooks/useSearchNews';
import { FilterContext } from '../../providers/FilterProvider';
import Button from '../ui/button/Button';
import Checkbox from '../ui/checkbox/Checkbox';
import styles from './WindowFilter.module.scss';
import { arrCategory, arrMiscellaneous, arrSource } from './checkbox.data';

const WindowFilter = () => {
	const { setIsViewFilter } = useFilter(FilterContext);
	const { register, handleSubmit, onSubmit, result } = useSearchNews();

	return (
		<div className={styles.wrapper}>
			<button
				className={styles.exit__button}
				onClick={() => setIsViewFilter(false)}
			>
				<img src='./images/icons/exit_edit.svg' alt='img' />
			</button>
			<form onSubmit={handleSubmit(onSubmit)}>
				<div className={styles.block__category}>
					<h2>Категории</h2>
					<div className={styles.block__checkbox}>
						{arrCategory.map(checkbox => {
							return (
								<Checkbox key={checkbox} id={checkbox} register={register}>
									{checkbox}
								</Checkbox>
							);
						})}
					</div>
				</div>
				<div className={styles.block__check_and_calendar}>
					<div className={styles.block__miscellaneous}>
						<h2>разное</h2>
						<div className={styles.block__checkbox}>
							{arrMiscellaneous.map(checkbox => {
								return (
									<Checkbox key={checkbox} id={checkbox} register={register}>
										{checkbox}
									</Checkbox>
								);
							})}
						</div>
					</div>
				</div>
				<div className={styles.block__source}>
					<h2>Источники</h2>
					<div className={styles.block__checkbox}>
						{arrSource.map(checkbox => {
							return (
								<Checkbox key={checkbox} id={checkbox} register={register}>
									{checkbox}
								</Checkbox>
							);
						})}
					</div>
				</div>
				<div className={styles.block__buttons}>
					<Button saveInfo='filter-clear'>очистить</Button>
					<Button saveInfo='filter-start' result={result}>
						применить
					</Button>
				</div>
			</form>
		</div>
	);
};

export default WindowFilter;
