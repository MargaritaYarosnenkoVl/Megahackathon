import { useMemo } from 'react';
import { useForm } from 'react-hook-form';
import { authService } from '../services/auth.service';
import { useAuth } from './useAuth';

export const useAuthPage = () => {
	const { setIsAuth } = useAuth();

	const {
		register,
		handleSubmit,
		// getValues,
		formState: { errors },
	} = useForm({ mode: 'onChange' });

	const onSubmit = async data => {
		authService.main(data.email, data.password, setIsAuth);
		console.log(data);
	};

	return useMemo(() => {
		return {
			onSubmit,
			register,
			handleSubmit,
			errors,
		};
	});
};
