/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   pruning_phase2.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: astripeb <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2021/05/30 12:59:06 by astripeb          #+#    #+#             */
/*   Updated: 2021/06/02 22:45:13 by astripeb         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

# include <stdint.h>
# include <stdio.h>

void	create_phase2_prun(int8_t *co_ud_edges_depth, int32_t *move_ud_edges,
	int32_t *move_corners, int32_t *co_classidx, int32_t *co_sym_idx,
	int32_t *co_sym, int32_t *co_rep, int32_t *conj_ud_edges)
{
	co_ud_edges_depth[0] = 0;
	for (int depth = 0; depth < 10; ++depth)
	{
		printf("Depth - %d done\n", depth);
		for (int classidx = 0; classidx < 2768; classidx++)
		{
			for (int ud_edge = 0; ud_edge < 40320; ud_edge++)
			{
				if (co_ud_edges_depth[40320 * classidx + ud_edge] == depth)
				{
					int corner = co_rep[classidx];
					for(int move = 0; move < 18; move++)
					{
						if (move == 3 || move == 5 || move == 6 || move == 8 || move == 12 || move == 14 || move == 15 || move == 17)
							continue;

						int ud_edge1 = move_ud_edges[18 * ud_edge + move];
						int corner1 = move_corners[18 * corner + move];

						int classidx1 = co_classidx[corner1];
						int co_sym1 = co_sym_idx[corner1];

						ud_edge1 = conj_ud_edges[16 * ud_edge1 + co_sym1];
						if (co_ud_edges_depth[40320 * classidx1 + ud_edge1] == 20)
						{
							co_ud_edges_depth[40320 * classidx1 + ud_edge1] = depth + 1;
							int sym = co_sym[classidx1];
							if (sym != 1)
							{
								for (int j = 1; j < 16; j++)
								{
									sym >>= 1;
									if (sym & 1)
									{
										int ud_edge2 = conj_ud_edges[16 * ud_edge1 + j];
										if (co_ud_edges_depth[40320 * classidx1 + ud_edge2] == 20)
											co_ud_edges_depth[40320 * classidx1 + ud_edge2] = depth + 1;
									}
								}
							}
						}
					}
				}
			}
		}
	}
}
