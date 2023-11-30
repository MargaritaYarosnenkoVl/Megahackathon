import React from "react";
import styles from './UserList.module.scss';
import { Link } from "react-router-dom";

const Pagination = (props) => {
    let pageNumbers = [];

    for (let i = 1; i <= Math.ceil(props.totalUsers / props.usersPerPage); i ++) {
        pageNumbers.push(i);
    };

    return (
        <div className={styles.block__pagination}>
            <ul className="pagination">
                {/* <li>
                    <Link onClick={props.prevPage}>
                        prevPage
                    </Link>
                </li>
                <li>
                    <Link onClick={props.nextPage}>
                        nextPage
                    </Link>
                </li> */}
                {
                    pageNumbers.map(number => (
                        <li key={number}>
                            <Link onClick={() => props.paginate(number)}>
                                {number}
                            </Link>
                        </li>
                    ))
                }
            </ul>
        </div>
    )
}

export default Pagination;
