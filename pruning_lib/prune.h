/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   prune.h                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: astripeb <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2021/06/02 22:36:54 by astripeb          #+#    #+#             */
/*   Updated: 2021/06/06 10:20:23 by astripeb         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef PRUNE_H
# define PRUNE_H

# include <stdint.h>
# include <stdio.h>

typedef struct s_phase2
{
	int			classidx;
	int			co_sym;
	int			ud_edge;
	int			corner;
	int			depth;
}				t_phase2;

typedef struct s_tables2
{
	int8_t		*co_depth;
	int32_t		*move_ud_edges;
	int32_t		*move_corners;
	int32_t		*co_classidx;
	int32_t		*co_sym_idx;
	int32_t		*co_sym;
	int32_t		*co_rep;
	int32_t		*conj_ud_edges;
}				t_tables2;

typedef struct s_phase1
{
	int			done;
	int			depth;
	int			fs;
	int			classidx;
	int			fs_sym;
	int			twist;
	int			flip;
	int			slice;
}				t_phase1;

typedef struct s_tables1
{
	int8_t		*fs_twist_depth;
	int32_t		*move_twist;
	int32_t		*move_flip;
	int32_t		*move_slice_sorted;
	int32_t		*conj_twist;
	int32_t		*fs_classidx;
	int32_t		*fs_sym_idx;
	int32_t		*fs_sym;
	int32_t		*fs_rep;
}				t_tables1;

#endif
