/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   prune_phase2_norm.c                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: astripeb <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2021/06/02 22:42:09 by astripeb          #+#    #+#             */
/*   Updated: 2021/06/03 23:08:36 by astripeb         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

# include "prune.h"

static t_tables2	get_tables(int8_t *co_ud_edges_depth, int32_t *moves,
					int32_t *co_classidx, int32_t *conj_ud_edges)
{
	t_tables2	tables;

	tables.co_depth = co_ud_edges_depth;
	tables.conj_ud_edges = conj_ud_edges;
	tables.move_corners = moves;
	tables.move_ud_edges = &moves[40320 * 18];
	tables.co_classidx = co_classidx;
	tables.co_sym_idx = &co_classidx[40320];
	tables.co_sym = &co_classidx[2 * 40320];
	tables.co_rep = &co_classidx[2 * 40320 + 2768];

	return (tables);
}

static void			check_symmetries(t_tables2 *tables, t_phase2 *vars)
{
	int i;
	int sym;
	int ud_edge;
	int idx;

	idx = 40320 * vars->classidx + vars->ud_edge;
	tables->co_depth[idx] = vars->depth + 1;
	sym = tables->co_sym[vars->classidx];
	if (sym != 1)
	{
		i = 1;
		while (i < 16)
		{
			sym >>= 1;
			if (sym & 1)
			{
				ud_edge = tables->conj_ud_edges[16 * vars->ud_edge + i];
				idx = 40320 * vars->classidx + ud_edge;
				if (tables->co_depth[idx] == 20)
					tables->co_depth[idx] = vars->depth + 1;
			}
			++i;
		}
	}
}

static void 		check_depth(t_tables2 *tables, t_phase2 *vars)
{
	int			m;
	int			corner;
	t_phase2	v2;

	m = 0;
	v2.depth = vars->depth;
	corner = tables->co_rep[vars->classidx];
	while (m < 18)
	{
		if (m == 3 || m == 5 || m == 6 || m == 8 || m == 12 \
			|| m == 14 || m == 15 || m == 17)
		{
			++m;
			continue;
		}
		v2.ud_edge = tables->move_ud_edges[18 * vars->ud_edge + m];
		v2.corner = tables->move_corners[18 * corner + m];
		v2.classidx = tables->co_classidx[v2.corner];
		v2.co_sym = tables->co_sym_idx[v2.corner];
		v2.ud_edge = tables->conj_ud_edges[16 * v2.ud_edge + v2.co_sym];
		if (tables->co_depth[40320 * v2.classidx + v2.ud_edge] == 20)
			check_symmetries(tables, &v2);
		m += 1;
	}
}

void				create_phase2_prun_norm(int8_t *co_ud_edges_depth,
	int32_t *moves, int32_t *co_classidx, int32_t *conj_ud_edges)
{
	t_phase2	v1;
	t_tables2	tables;

	tables = get_tables(co_ud_edges_depth, moves, co_classidx, conj_ud_edges);
	tables.co_depth[0] = 0;
	v1.depth = 0;
	while (v1.depth < 10)
	{
		v1.classidx = 0;
		while (v1.classidx < 2768)
		{
			v1.ud_edge = 0;
			while (v1.ud_edge < 40320)
			{
				if (tables.co_depth[40320 * v1.classidx + v1.ud_edge] \
					== v1.depth)
					check_depth(&tables, &v1);
				v1.ud_edge += 1;
			}
			v1.classidx += 1;
		}
		v1.depth += 1;
	}
}
