/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   pruning_phase1.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: astripeb <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2021/05/30 22:34:56 by astripeb          #+#    #+#             */
/*   Updated: 2021/06/06 11:42:47 by astripeb         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "prune.h"

static t_tables1	get_tables(int8_t *fs_twist_depth, int32_t *moves,
					int32_t *conj_twist, int32_t *fs_classidx)
{
	t_tables1	tables;

	tables.fs_twist_depth = fs_twist_depth;
	tables.move_twist = moves;
	tables.move_flip = &moves[18 * 2187];
	tables.move_slice_sorted = &moves[18 * 2187 + 18 * 2048];
	tables.conj_twist = conj_twist;
	tables.fs_classidx = fs_classidx;
	tables.fs_sym_idx = &fs_classidx[495 * 2048];
	tables.fs_sym = &fs_classidx[495 * 2048 * 2];
	tables.fs_rep = &fs_classidx[495 * 2048 * 2 + 64430];
	return (tables);
}

static void	check_symmetries(t_tables1 *t, t_phase1 *v, int *done)
{
	int		i;
	int		sym;
	int		tw1;

	t->fs_twist_depth[2187 * v->classidx + v->twist] = v->depth + 1;
	*done += 1;
	sym = t->fs_sym[v->classidx];
	if (sym != 1)
	{
		i = 1;
		while (i < 16)
		{
			sym >>= 1;
			if (sym & 1)
			{
				tw1 = t->conj_twist[16 * v->twist + i];
				if (t->fs_twist_depth[2187 * v->classidx + tw1] == 20)
				{
					t->fs_twist_depth[2187 * v->classidx + tw1] = v->depth + 1;
					*done += 1;
				}
			}
			++i;
		}
	}
}

static void	check_depth(t_tables1 *t, t_phase1 *v1)
{
	int			move;
	t_phase1	v2;

	v1->fs = t->fs_rep[v1->classidx];
	v1->flip = v1->fs & 0x7FF;
	v1->slice = v1->fs >> 11;
	v2.depth = v1->depth;
	move = 0;
	while (move < 18)
	{
		v2.twist = t->move_twist[18 * v1->twist + move];
		v2.flip = t->move_flip[18 * v1->flip + move];
		v2.slice = t->move_slice_sorted[432 * v1->slice + move] / 24;
		v2.fs = (v2.slice << 11) + v2.flip;
		v2.classidx = t->fs_classidx[v2.fs];
		v2.fs_sym = t->fs_sym_idx[v2.fs];
		v2.twist = t->conj_twist[16 * v2.twist + v2.fs_sym];
		if (t->fs_twist_depth[2187 * v2.classidx + v2.twist] == 20)
			check_symmetries(t, &v2, &v1->done);
		move += 1;
	}
}

void	create_phase1_prun(int8_t *fs_twist_depth, int32_t *moves,
		int32_t *conj_twist, int32_t *fs_classidx)
{
	t_phase1	v1;
	t_tables1	t;

	t = get_tables(fs_twist_depth, moves, conj_twist, fs_classidx);
	fs_twist_depth[0] = 0;
	v1.done = 1;
	v1.depth = 0;
	while (v1.done < 64430 * 2187)
	{
		v1.classidx = 0;
		while (v1.classidx < 64430)
		{
			v1.twist = 0;
			while (v1.twist < 2187)
			{
				if (t.fs_twist_depth[2187 * v1.classidx + v1.twist]
					== v1.depth)
					check_depth(&t, &v1);
				v1.twist += 1;
			}
			v1.classidx += 1;
		}
		v1.depth += 1;
	}
}
