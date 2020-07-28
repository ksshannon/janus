"""
Created on Tue Jul  9 12:12:43 2019

@author: lejoflores
"""

import numpy as np
import scipy.special as sp
# TODO import IM3agents.im3networks as nwk
# collab w Chris Vernon to get package right?

def define_seed(seed):
    """ Creates seed for random selection for testing
    :param seed:            Seed value

    :return:                Global seed value

    """
    global seed_val

    seed_val = seed

    return


def switching_prob_curve(alpha, beta, fmin, fmax, n, profit):
    """ Creates probability curves that show likelyhood of switching crops based on profits"
    :param alpha: The alpha parameter for the incomplete beta distribution
    :param beta: The beta parameter for the incomplete beta distribution
    :param fmin: The fraction of current profit at which the CDF of the beta distribution is zero
    :param fmax: The fraction of current profit at which the CDF of the beta distribution is one
    :param n: The number of points to generate in the CDF
    :param profit: The current profit of the farmer

    :return: Two (n x 1) numpy arrays containing, respectively n points spaced
             linearly between fmin*profit and fmax*profit (x2) and the associated points
             of the beta distribution as specified by alpha and beta (fx).

    """
    x = np.linspace(0, 1.0, num=n)

    fx = sp.betainc(alpha, beta, x)

    x2 = np.linspace(fmin * profit, fmax * profit, num=n)

    return x2, fx



def retrieve_network_profits(agentID, ):
    """
    This will be called in the main model to retrieve the array of profits
    based upon the agent ID

    :param agentID:        agentID for the agent whose network to retrieve
    :type agentID:         int

    :return: a 2D array of cropIDs and their associated profits in the network of agent

    """
    # TODO pass in crops and profit arrays -- see assess_profits
    # TODO - change this to call actual network
    temp_network = np.random.randint(0, size=4)
    # might look something like
    # network_ids =

    # at this point now there should be a list of agents in that network

    # for each of those agents
        # retrieve crop ID? or retrieve profit?
        # see Kendra's notes in Slack
        # in the model.py it will be crop_id_all[i-1, :, :]
        # then index into specific j,k values from agentID
        # this will need to be passed in



def success_bias_decision():
    """


    Returns
    -------
    None.

    """
    # pick max profit and associated cropID

    # put that into the decide2switch function

    # return the cropID they are going with (either their current or the most successful)
    # and the profit associated with each




# conformist bias
# inputs: d = the strength of conformity bias (0-1)
# observe their network, and calculate the proportion of each crop
# select the crop w the highest proportion (p)
# eqn from example p * 1/d
# return: cropID
# if n of network is less than n of crops then high likelihood that there are no repeat crops then... ?
# a realistic social network is connected to 3-4 ppl...
# given the number of alternative crops, does CB make sense?
# and/or is there an alternative "characteristic" that individuals could conform to


def decide(alpha, beta, fmin, fmax, n, profit, profit_p):
    """ This decides whether to retain current crop or switch to one other option

    :param alpha: The alpha parameter for the incomplete beta distribution
    :param beta: The beta parameter for the incomplete beta distribution
    :param fmin: The fraction of current profit at which the CDF of the beta distribution is zero
    :param fmax: The fraction of current profit at which the CDF of the beta distribution is one
    :param n: The number of points to generate in the CDF
    :param profit: The current profit the farmer experiences
    :param profit_p: The potential profit of the alternative crop being evaluated

    :return: A binary flag indicating whether or not to switch crops (1 = switch, 0 = do not switch)

    """
    if profit_p > profit:

        x, fx = switching_prob_curve(alpha, beta, fmin, fmax, n, profit)

        prob_switch = np.interp(profit_p, x, fx)

        if (np.random.rand(1) < prob_switch):  # need to send it seed in the unit test
            return 1  # Switch
        else:
            return 0  # Do not switch

    else:
        return 0  # Do not switch if not profitable


def assess_profit(crop, profits_current, profit_signals, num_crops, crop_ids):
    """A given location, get the potential profits from the next time step and set the last profit equal to the current profit

   :param crop:             Current crop choice
   :type crop:              Int

   :param profits_current:  Profit from current crop choice
   :type profits_current:   Float

   :param profit_signals:   A vector of profits against which current profit will be assessed
   :type profit_signals:    Vector

   :param num_crops:        The number of crops in the vector of Profit_signals
   :type num_crops:         Int

   :param crop_ids:          The associated vector of crop IDs associated with the input profit signal
   :param crop_ids:          Vector

   :return:                 [0] Float; profit for a particular crop (Crop) from the last time step
                            [1] Numpy array; potential profits for the current time step

   """

    # Existing Crop ID
    cur_crop_choice_ind = crop.astype('int')

    # assess current and future profit of that given crop
    if np.isin(cur_crop_choice_ind, crop_ids):  # if the current land cover is a crop
        profit_last = profits_current  # last years profit in this location
        profit_expected = profit_signals.reshape(num_crops, 1)  # next years anticipated profit

    else:
        profit_last = 0
        profit_expected = np.zeros((num_crops, 1))

    return profit_last, profit_expected


def profit_maximizer(alpha, beta, fmin, fmax, n, profits_current, vec_crops, vec_profit_p, rule=True):
    """ Decide which crop and associated profit to pick out of N options.
    Only used for the profit maximization crop decision rule.

    :param alpha:           Alpha parameter for the incomplete beta distribution
    :type alpha:            Float

    :param beta:            Beta parameter for the incomplete beta distribution
    :type beta:             Float

    :param fmin:            Fraction of current profit at which the CDF of the beta distribution is zero
    :type fmin:             Int

    :param fmax:            Fraction of current profit at which the CDF of the beta distribution is one
    :type fmax:             Int

    :param n:               Number of points to generate in the CDF
    :type n:                Int

    :param alpha: The alpha parameter for the incomplete beta distribution
    :param beta: The beta parameter for the incomplete beta distribution
    :param fmin: The fraction of current profit at which the CDF of the beta distribution is zero
    :param fmax: The fraction of current profit at which the CDF of the beta distribution is one
    :param n: The number of points ato generate in the CDF
    :param current_profit: The current profit the farmer experiences
    :param vec_crops: A vector of potential alternative crops
    :param vec_profit_p: A vector of potential profits associated with the alternatives contained in vec_crops
    :param rule: A boolean indicating whether, if multiple alternative crops are viably \
                 more profitable, to choose the most profitable alternative (True),
                 or select randomly between all viable alternatives.

    :return: integer denoting crop choice and float of the associated profit
    """

    # Key assumptions: the vector of crop IDs and anticipated profits associated
    # with each crop must both be N x 1 column vectors. Error trap this below:
    assert (vec_crops.shape == vec_profit_p.shape), \
        'Supplied vector of crop IDs and potential profits must be identical'
    assert (vec_crops.shape[1] == 1), \
        'Supplied vector of crop IDs and potential profits must be N x 1'

    # Create a boolean vector to store a 0 or 1 if the farmer will select the
    # crop (==1) or not (==1)
    AccRej = np.zeros(vec_crops.shape, dtype='int')

    for i in np.arange(AccRej.size):
        # Use the `Decide` function above to choose whether or not the crop is
        # viable
        AccRej[i] = decide(alpha, beta, fmin, fmax, n, Profits_current,
                           vec_profit_p[i])  # is fmin/fmax setting bounds on range of additional profit?

    # Find the Crop IDs and associated profits that were returned as "viable"
    # based on the "Decide" function (that is, Decide came back as "yes" == 1)
    ViableCrops = vec_crops[AccRej == 1]
    ViableProfits = vec_profit_p[AccRej == 1]

    if (ViableCrops.size == 0):
        return -1, -1

    # Find the maximum anticipated profit and the crop IDs associated with that
    # maximum
    MaxProfit = ViableProfits.max()
    MaxProfitCrop = ViableCrops[ViableProfits == MaxProfit]

    # This next part should be rare. There happen to be more than one viable
    # crops that carry the same anticipated profit that also coincides with
    # the maximum anticipated profit. The choice here is to choose randomly
    # from among those crops that have the same (maximum) profit
    if (MaxProfitCrop.size > 1):
        ViableCrops = MaxProfitCrop
        ViableProfits = ViableProfits[ViableProfits == MaxProfit]
        rule = False  # Switch rule to trick the algorithm into using the random option

    if (rule):  # Return crop with largest profit
        CropChoice = MaxProfitCrop
        ProfitChoice = MaxProfit

    else:  # Choose randomly from among all viable crops
        indChoice = np.random.choice(np.arange(ViableCrops.size), size=1)
        CropChoice = ViableCrops[indChoice]
        ProfitChoice = ViableProfits[indChoice]

    # Return the crop choice and associated profit
    return CropChoice, ProfitChoice


def assess_profit(Crop, Profits_current, Profit_signals, Num_crops, CropIDs):
    """Get the potential profits from the next time step and set the last profit equal to the current profit

   :param Crop: Current crop choice
   :param Profits_current: Profit from current crop choice
   :param Profit_signals: A vector of profits against which current profit will be assessed
   :param Num_crops: The number of crops in the vector of Profit_signals
   :param CropIDs: The associated vector of crop IDs associated with the input profit signal

   :return: float of the profit for a particular crop (Crop) from the last time step, and an array of potential profits for the current time step

   """

    # Existing Crop ID
    CurCropChoice_ind = Crop.astype('int')
    # CropIx=np.where(CropIDs == CurCropChoice_ind)# crop ID lookup
    # assess current and future profit of that given crop
    if np.isin(CurCropChoice_ind, CropIDs):  # if the current landcover is a crop
        Profit_last = Profits_current  # last years profit in this location
        Profit_expected = Profit_signals.reshape(Num_crops, 1)

    else:
        Profit_last = 0
        Profit_expected = np.zeros((Num_crops, 1))

    return Profit_last, Profit_expected


def make_choice(CropID_last, Profit_last, CropChoice, ProfitChoice, seed=False):
    """ Compare the crop choice with associated profit and crop choice switches and set the new crop ID if switching

    :param CropID_last: The crop choice from the last time step
    :param Profit_last: The profit from the last time step associated with that crop
    :param CropChoice: A flag indicating whether the new crop is selected
    :param ProfitChoice: A flag indicating whether there is a profitable alternative
    :param seed: A boolean indicating whether or not to use a random seed

    :return: The new crop ID and its associated profit
    """

    if seed:

        try:
            seed_val
        except NameError:
            print("Random seed needs to be initialized using the CropDecider.DefineSeed() Function")

        np.random.seed(seed_val)

    # Check if return  values indicate the farmer shouldn't switch
    if (CropChoice == -1) and (ProfitChoice == -1):
        CropID_next = CropID_last
        Profit_act = Profit_last + np.random.normal(loc=0.0, scale=1000.0, size=(1, 1, 1))  # this years actual profit

    else:  # switch to the new crop
        CropID_next = CropChoice
        Profit_act = ProfitChoice + np.random.normal(loc=0.0, scale=1000.0, size=(1, 1, 1))

    return CropID_next, Profit_act
