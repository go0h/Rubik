GREEN 				:= \033[0;32m
RED 				:= \033[0;31m
RESET				:= \033[0m
BLINK				:= \033[5m
NORMAL				:= \033[25m
BOLDU				:= \033[1m\033[4m

NAME				:= pruning.so

#COMPILER
CC 					:= gcc

#PROJECT_DIRS
SRC_DIR				:= ./pruning_lib
OBJ_DIR				:= $(SRC_DIR)/.obj


#COMPILER FLAGS
CFLAGS				?= -Wall -Wextra -Werror -O3
DEPEND				:= -MD -MT


################################################################################
#									SOURCE FILES					 		   #
################################################################################

SRC					:= pruning_phase1.c pruning_phase2.c

################################################################################
#																	 		   #
################################################################################

OBJ					:= $(SRC:.c=.o)

vpath %.c $(SRC_DIR)
vpath %.o $(OBJ_DIR)
vpath %.so $(SRC_DIR)

all: $(NAME)

$(NAME): $(OBJ)
	$(CC) $(CFLAGS) -shared -fPIC $(addprefix $(OBJ_DIR)/, $(OBJ)) -o $(SRC_DIR)/$@
	echo "$(GREEN)Creating $(BOLDU)$@$(RESET)"
	echo "$(GREEN)$(BLINK)DONE✅$(NORMAL)$(RESET)"

$(OBJ):%.o:%.c | $(OBJ_DIR)
	$(CC) $(CFLAGS) -c $< -o $(OBJ_DIR)/$@ $(DEPEND) $@
	echo "$(GREEN)Creating $(BOLDU)$@$(RESET)"

$(OBJ_DIR):
	mkdir -p $@

clean:
	rm -rf $(OBJ_DIR)
	echo "$(RED)Deleting $(BOLDU)objs files$(RESET)"

fclean: clean
	rm -rf $(SRC_DIR)/$(NAME)
	echo "$(RED)Deleting $(BOLDU)$(NAME)$(RESET)"

re: fclean all

include $(wildcard $(OBJ_DIR)/*.d)

.SILENT: all clean re fclean $(NAME) $(OBJ) $(OBJ_DIR)

.PHONY: clean fclean re all
