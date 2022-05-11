# This module will determine the berthing velocity of a vessel
# as a function of it's loaded displacement and exposure condition.
# The Equations below represent a power curve fit of the charts
# provided in UFC 4-152-01

def velocity(disp, cond):
    # Determine berthing velocity:
    # Definition:
    #   disp    = Vessel displacement (LT)
    #   cond    = Berthing condition
    #       sheltered, moderate, or exposed

    match cond:
        case "sheltered":
            vel = 4.1172 * disp**(-0.289)
        case "moderate":
            vel = 8.9392 * disp**(-0.302)
        case "exposed":
            vel = 10.9182 * disp**(-0.2802)
    return vel
