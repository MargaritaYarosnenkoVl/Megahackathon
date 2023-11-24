import { useMemo } from 'react';
import { useForm } from 'react-hook-form';

export const useEditNews = () => {
	const { register, handleSubmit, getValues } = useForm({ mode: 'onChange' });

	const onSubmit = data => {
		console.log('edit news', data);
	};

	return useMemo(() => {
		return {
			register,
			handleSubmit,
			onSubmit,
			getValues,
		};
	});
};
