/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   pruning_phase1.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: astripeb <marvin@42.fr>                    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2021/05/30 22:34:56 by astripeb          #+#    #+#             */
/*   Updated: 2021/05/30 23:26:24 by astripeb         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

# include <stdint.h>
# include <stdio.h>

void	create_phase1_prun(int8_t *fs_twist_depth,
		int32_t *move_twist, int32_t *move_flip, int32_t *move_slice_sorted,
		int32_t *conj_twist, int32_t *fs_classidx, int32_t *fs_sym_idx,
		int32_t *fs_sym, int32_t *fs_rep)
{
	fs_twist_depth[0] = 0;
	int done = 1;
	int depth = 0;
	char back_search = 0;
	while (done < 64430 * 2187)
	{
		printf("Depth - %d done\n", depth);

		if (depth == 9)
			back_search = 1;

		for (int classidx = 0; classidx < 64430; ++classidx)
		{
			for (int twist = 0; twist < 2187; ++twist)
			{
				char match = 0;
				if (back_search)
					match = fs_twist_depth[2187 * classidx + twist] == 20;
				else
					match = fs_twist_depth[2187 * classidx + twist] == depth;

				if (match)
				{
					int fs = fs_rep[classidx];
					int flip = fs & 0x7FF;     // fs % 2048
					int slice = fs >> 11;      // fs  2048

					for (int move = 0; move < 18; ++move)
					{

						int twist1 = move_twist[18 * twist + move];
						int flip1 = move_flip[18 * flip + move];
						int slice1 = move_slice_sorted[432 * slice + move] / 24;

						int fs1 = (slice1 << 11) + flip1;
						int classidx1 = fs_classidx[fs1];
						int fs_sym1 = fs_sym_idx[fs1];

						twist1 = conj_twist[16 * twist1 + fs_sym1];

						if (!back_search)
						{
							if (fs_twist_depth[2187 * classidx1 + twist1] == 20)
							{
								fs_twist_depth[2187 * classidx1 + twist1] = depth + 1;
								++done;

								int sym = fs_sym[classidx1];
								if (sym != 1)
								{
									for (int j = 1; j < 16; ++j)
									{
										sym >>= 1;
										if (sym & 1)
										{
											int twist2 = conj_twist[16 * twist1 + j];
											if (fs_twist_depth[2187 * classidx1 + twist2] == 20)
											{
												fs_twist_depth[2187 * classidx1 + twist2] = depth + 1;
												++done;
											}
										}
									}
								}
							}
						}
						else
						{
							if (fs_twist_depth[2187 * classidx1 + twist1] == depth)
							{
								fs_twist_depth[2187 * classidx + twist] = depth + 1;
								++done;
								break;
							}
						}
					}
				}
			}
		}
		++depth;
	}
}

