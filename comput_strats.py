import numpy as np


# return a 2-dim array of size [nb_boxes^nb_steps,nb_steps]
def generate_player_strats(nb_steps: int, nb_boxes: int) -> np.ndarray:
    if nb_steps == 1:
        return np.expand_dims(np.arange(nb_boxes), axis=-1)
    else:
        n_minus_1_strats: np.ndarray = generate_player_strats(nb_steps-1, nb_boxes)
        all_strats = np.empty((0, nb_steps))
        for i in range(nb_boxes):

            first_step_i = np.full((n_minus_1_strats.shape[0], 1), i)
            strats_with_first_step_i = np.concatenate((first_step_i, n_minus_1_strats), axis=-1)
            all_strats = np.concatenate((all_strats, strats_with_first_step_i), axis=0)
        return all_strats

def generate_rabbit_strats(nb_steps: int, nb_boxes: int) -> np.ndarray:

    if nb_steps == 1:
        return np.expand_dims(np.arange(nb_boxes), axis=-1)
    else:
        n_minus_1_strats: np.ndarray = generate_rabbit_strats(nb_steps-1, nb_boxes)
        left_compatibles_strats = n_minus_1_strats[n_minus_1_strats[:, -1] >= 1, :]
        right_compatibles_strats = n_minus_1_strats[n_minus_1_strats[:, -1] < nb_boxes - 1, :]

        left_moves = np.expand_dims(left_compatibles_strats[:, -1] - 1, axis=-1)
        right_moves = np.expand_dims(right_compatibles_strats[:, -1] + 1, axis=-1)

        left_strats = np.concatenate((left_compatibles_strats, left_moves), axis=-1)
        right_strats = np.concatenate((right_compatibles_strats, right_moves), axis=-1)
        all_strats = np.concatenate((left_strats, right_strats), axis=0)
        return all_strats


def find_best_strats(nb_boxes: int) -> np.ndarray:

    nb_steps = 1
    while True:
        player_strats = generate_player_strats(nb_steps, nb_boxes)
        rabbit_strats = generate_rabbit_strats(nb_steps, nb_boxes)
        nb_player_strats = player_strats.shape[0]

        winner_strats = []
        for idx_player_strat in range(nb_player_strats):
            found_rabbit = rabbit_strats == player_strats[idx_player_strat]
            found_rabbit_on_all_strats: bool = np.all(np.any(found_rabbit, axis=-1))
            if found_rabbit_on_all_strats:
                winner_strats.append(player_strats[idx_player_strat])
        if len(winner_strats) > 0:
            return winner_strats
        nb_steps += 1


for nb_boxes in range(3,7):
    print(f"best strats with {nb_boxes} boxes: {find_best_strats(nb_boxes)}")
