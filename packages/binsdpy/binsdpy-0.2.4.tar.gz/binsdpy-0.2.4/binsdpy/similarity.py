import math

from binsdpy.utils import (
    operational_taxonomic_units,
    BinaryFeatureVector,
    BinaryFeatureVectorEmpty,
)


def dice1(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Dice 1 similarity (v1)

    Dice, L. R. (1945).
    Measures of the amount of ecologic association between species.
    Ecology, 26(3), 297-302

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, _, _ = operational_taxonomic_units(x, y, mask)

    return a / (a + b)


def dice2(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Dice 2 similarity (v2)

    Dice, L. R. (1945).
    Measures of the amount of ecologic association between species.
    Ecology, 26(3), 297-302

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, _, c, _ = operational_taxonomic_units(x, y, mask)

    return a / (a + c)


def jaccard(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Jaccard similarity

    Same as:
        Tanimoto coefficient

    Jaccard, P. (1908).
    Nouvelles recherches sur la distribution florale.
    Bull. Soc. Vaud. Sci. Nat., 44, 223-270.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, _ = operational_taxonomic_units(x, y, mask)

    return a / (a + b + c)


def sw_jaccard(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """SW Jaccard similarity

    Jaccard, P. (1908).
    Nouvelles recherches sur la distribution florale.
    Bull. Soc. Vaud. Sci. Nat., 44, 223-270.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, _ = operational_taxonomic_units(x, y, mask)

    return (3 * a) / (3 * a + b + c)


def gleason(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Gleason similarity

    Gleason, H. A. (1920).
    Some applications of the quadrat method.
    Bulletin of the Torrey Botanical Club, 47(1), 21-33.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, _ = operational_taxonomic_units(x, y, mask)

    return (2 * a) / (2 * a + b + c)


def kulczynski1(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Kulczynski similarity (v1)

    Stanisław Kulczynśki. (1927).
    Die pflanzenassoziationen der pieninen.
    Bulletin International de l'Academie Polonaise des Sciences et des Lettres, Classe des Sciences Mathematiques et Naturelles, B (Sciences Naturelles), pages 57–203.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, _ = operational_taxonomic_units(x, y, mask)

    return a / (b + c)


def kulczynski2(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Kulczynski similarity (v2)

    Stanisław Kulczynśki. (1927).
    Die pflanzenassoziationen der pieninen.
    Bulletin International de l'Academie Polonaise des Sciences et des Lettres, Classe des Sciences Mathematiques et Naturelles, B (Sciences Naturelles), pages 57–203.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, _ = operational_taxonomic_units(x, y, mask)

    return 0.5 * (a / (a + b) + a / (a + c))


def cosine(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Cosine similarity

    Same as:
        Ochiai similarity
        Otsuka similarity

    Ochiai, A. (1957).
    Zoogeographic studies on the soleoid fishes found in Japan and its neighbouring regions.
    Bulletin of Japanese Society of Scientific Fisheries, 22, 526-530.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """

    a, b, c, _ = operational_taxonomic_units(x, y, mask)

    return a / math.sqrt((a + b) * (a + c))


def braun_blanquet(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Braun-Banquet similarity

    Braun-Blanquet, J. (1932).
    Plant sociology. The study of plant communities. Plant sociology.
    The study of plant communities. First ed.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, _ = operational_taxonomic_units(x, y, mask)

    return a / max(a + b, a + c)


def simpson(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Simpson similarity

    Simpson, E. H. (1949).
    Measurement of diversity.
    Nature, 163(4148), 688-688.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, _ = operational_taxonomic_units(x, y, mask)

    return a / min(a + b, a + c)


def sorgenfrei(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Sorgenfrei similarity

    Sorgenfrei, T. (1958).
    Molluscan Assemblages from the Marine Middle Miocene of South Jutland and their Environments. Vol. II.
    Danmarks Geologiske Undersøgelse II. Række, 79, 356-503.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, _ = operational_taxonomic_units(x, y, mask)

    return (a * a) / ((a + b) * (a + c))


def mountford(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Mountford similarity

    Mountford, M. D. (1962).
    An index of similarity and its application to classificatory problem.
    Progress in soil zoology"(ed. Murphy, PW), 43-50.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, _ = operational_taxonomic_units(x, y, mask)

    return (2 * a) / (a * b + a * c + 2 * b * c)


def fager_mcgowan(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Fager-McGowan similarity

    Fager, E. W. (1957).
    Determination and analysis of recurrent groups.
    Ecology, 38(4), 586-595.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, _ = operational_taxonomic_units(x, y, mask)

    return a / math.sqrt((a + b) * (a + c)) - max(a + b, a + c) / 2


def sokal_sneath1(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Sokal-Sneath similarity (v1)

    Sneath, P. H., & Sokal, R. R. (1973).
    Numerical taxonomy.
    The principles and practice of numerical classification.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, _ = operational_taxonomic_units(x, y, mask)

    return a / (a + 2 * b + 2 * c)


def mcconnaughey(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """McConnaughey similarity

    McConnaughey, B. H. (1964).
    The determination and analysis of plankton communities.
    Lembaga Penelitian Laut.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, _ = operational_taxonomic_units(x, y, mask)

    return (a * a - b * c) / ((a + b) * (a + c))


def johnson(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Johnson similarity

    Johnson, S. C. (1967).
    Hierarchical clustering schemes.
    Psychometrika, 32(3), 241-254.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, _ = operational_taxonomic_units(x, y, mask)

    return a / (a + b) + a / (a + c)


def van_der_maarel(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Van der Maarel similarity

    Van der Maarel, E. (1969).
    On the use of ordination models in phytosociology.
    Vegetatio, 19(1), 21-46.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, _ = operational_taxonomic_units(x, y, mask)

    return (2 * a - b - c) / (2 * a + b + c)


def consonni_todeschini4(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Consonni and Todeschini (v4)

    Consonni, V., & Todeschini, R. (2012).
    New similarity coefficients for binary data.
    Match-Communications in Mathematical and Computer Chemistry, 68(2), 581.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, _ = operational_taxonomic_units(x, y, mask)

    return math.log(1 + a) / math.log(1 + a + b + c)


def russell_rao(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Russel-Rao similarity

    Russell, P. F., & Rao, T. R. (1940).
    On habitat and association of species of anopheline larvae in south-eastern Madras.
    Journal of the Malaria Institute of India, 3(1).

    Rao, C. R. (1948).
    The utilization of multiple measurements in problems of biological classification.
    Journal of the Royal Statistical Society. Series B (Methodological), 10(2), 159-203.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return a / (a + b + c + d)


def consonni_todeschini3(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Consonni and Todeschini (v3)

    Consonni, V., & Todeschini, R. (2012).
    New similarity coefficients for binary data.
    Match-Communications in Mathematical and Computer Chemistry, 68(2), 581.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return math.log(1 + a) / math.log(1 + a + b + c + d)


def smc(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Sokal-Michener similarity (also called simple matching coefficient)

    Sokal, R. R. (1958).
    A statistical method for evaluating systematic relationships.
    Univ. Kansas, Sci. Bull., 38, 1409-1438.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (a + d) / (a + b + c + d)


def rogers_tanimoto(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Roges-Tanimoto similarity

    Rogers, D. J., & Tanimoto, T. T. (1960).
    A computer program for classifying plants.
    Science, 132(3434), 1115-1118.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (a + d) / (a + 2 * (b + c) + d)


def sokal_sneath2(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Sokal-Sneath similarity (v2)

    Sneath, P. H., & Sokal, R. R. (1973).
    Numerical taxonomy.
    The principles and practice of numerical classification.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (2 * (a + d)) / (2 * (a + d) + b + c)


def sokal_sneath3(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Sokal-Sneath similarity (v3)

    Sneath, P. H., & Sokal, R. R. (1973).
    Numerical taxonomy.
    The principles and practice of numerical classification.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (a + d) / (b + c)


def faith(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Faith similarity

    Faith, D. P. (1983).
    Asymmetric binary similarity measures.
    Oecologia, 57(3), 287-290.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (a + 0.5 * d) / (a + b + c + d)


def gower_legendre(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Gower-Legendre similarity

    Gower, J. C., & Legendre, P. (1986).
    Metric and Euclidean properties of dissimilarity coefficients.
    Journal of classification, 3(1), 5-48.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (a + d) / (a + 0.5 * (b + c) + d)


def gower(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Gower similarity

    Gower, J. C. (1971).
    A general coefficient of similarity and some of its properties.
    Biometrics, 857-871.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (a + d) / math.sqrt((a + b) * (a + c) * (b + d) * (c + d))


def austin_colwell(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Austin-Colwell similarity

    Austin, B., & Colwell, R. R. (1977).
    Evaluation of some coefficients for use in numerical taxonomy of microorganisms.
    International Journal of Systematic and Evolutionary Microbiology, 27(3), 204-210.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return 2 / math.pi * math.asin(math.sqrt((a + d) / (a + b + c + d)))


def consonni_todeschini1(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Consonni and Todeschini similarity (v1)

    Consonni, V., & Todeschini, R. (2012).
    New similarity coefficients for binary data.
    Match-Communications in Mathematical and Computer Chemistry, 68(2), 581.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return math.log(1 + a + d) / math.log(1 + a + b + c + d)


def hamman(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Hamman similarity

    Hamann, U. (1961).
    Merkmalsbestand und verwandtschaftsbeziehungen der farinosae: ein beitrag zum system der monokotyledonen.
    Willdenowia, 639-768.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (a + d - b - c) / (a + b + c + d)


def peirce1(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Peirce similarity (v1)

    Peirce, C. S. (1884).
    The numerical measure of the success of predictions.
    Science, (93), 453-454.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (a * d - b * c) / ((a + b) * (c + d))


def peirce2(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Peirce similarity (v2)

    Peirce, C. S. (1884).
    The numerical measure of the success of predictions.
    Science, (93), 453-454.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (a * d - b * c) / ((a + c) * (b + d))


def yuleq(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Yule's Q similarity

    Yule, G. U. (1912).
    On the methods of measuring association between two attributes.
    Journal of the Royal Statistical Society, 75(6), 579-652.

    Yule, G. U. (1900).
    On the association of attributes in statistics.
    Philosophical Transactions of the Royal Society. Series A, 194, 257-319.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (a * d - b * c) / (a * d + b * c)


def yulew(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Yule's W similarity

    Yule, G. U. (1912).
    On the methods of measuring association between two attributes.
    Journal of the Royal Statistical Society, 75(6), 579-652.

    Yule, G. U. (1900).
    On the association of attributes in statistics.
    Philosophical Transactions of the Royal Society. Series A, 194, 257-319.


    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (math.sqrt(a * d) - math.sqrt(b * c)) / (math.sqrt(a * d) + math.sqrt(b * c))


def pearson1(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Pearson Chi-Squared similarity

    Pearson, K., & Heron, D. (1913).
    On theories of association.
    Biometrika, 9(1/2), 159-315.

    Pearson, K. X. (1900).
    On the criterion that a given system of deviations from the probable in the case 538 of a correlated system of variables is such that it can be reasonably supposed to have arisen 539 from random sampling.
    London, Edinburgh, Dublin Philos. Mag. J. Sci, 540, 50.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    n = a + b + c + d

    return (n * ((a * d - b * c) ** 2)) / ((a + b) * (a + c) * (b + d) * (c + d))


def pearson2(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Pearson similarity (v2)

    Pearson, K., & Heron, D. (1913).
    On theories of association.
    Biometrika, 9(1/2), 159-315.

    Pearson, K. X. (1900).
    On the criterion that a given system of deviations from the probable in the case 538 of a correlated system of variables is such that it can be reasonably supposed to have arisen 539 from random sampling.
    London, Edinburgh, Dublin Philos. Mag. J. Sci, 540, 50.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    x_2 = pearson1(x, y, mask)

    return math.sqrt(x_2 / (a + b + c + d + x_2))


def phi(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Phi similarity

    Yule, G. U. (1912).
    On the methods of measuring association between two attributes.
    Journal of the Royal Statistical Society, 75(6), 579-652.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (a * d - b * c) / math.sqrt((a + b) * (a + c) * (b + d) * (c + d))


def michael(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Michael similarity

    Michael, E. L. (1920).
    Marine ecology and the coefficient of association: a plea in behalf of quantitative biology.
    Journal of Ecology, 8(1), 54-59.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return 4 * (a * d - b * c) / ((a + d) ** 2 + (b + c) ** 2)


def cole1(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Cole similarity (v1)

    Cole, L. C. (1957).
    The measurement of partial interspecific association.
    Ecology, 38(2), 226-233.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (a * d - b * c) / ((a + c) * (c + d))


def cole2(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Cole similarity (v2)

    Cole, L. C. (1957).
    The measurement of partial interspecific association.
    Ecology, 38(2), 226-233.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (a * d - b * c) / ((a + b) * (b + d))


def cole(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Cole similarity

    Cole, L. C. (1957).
    The measurement of partial interspecific association.
    Ecology, 38(2), 226-233.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    if (a * d) >= (b * c):
        return (a * d - b * c) / ((a + b) * (b + d))
    elif (a * d) < (b * c) and a <= d:
        return (a * d - b * c) / ((a + b) * (a + c))
    else:
        return (a * d - b * c) / ((b + d) * (c + d))


def cohen(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Cohen similarity

    Cohen, J. (1960).
    A coefficient of agreement for nominal scales.
    Educational and psychological measurement, 20(1), 37-46.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (2 * (a * d - b * c)) / math.sqrt((a + b) * (b + d) + (a + c) * (c + d))


def maxwell_pilliner(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Maxwell-Pilliner similarity

    Maxwell, A. E., & Pilliner, A. E. G. (1968).
    Deriving coefficients of reliability and agreement for ratings.
    British Journal of Mathematical and Statistical Psychology, 21(1), 105-116.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (2 * (a * d - b * c)) / ((a + b) * (c + d) + (a + c) * (b + d))


def dennis(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Dennis similarity

    Dennis, S. F. (1965).
    The Construction of a Thesaurus Automatically From.
    In Statistical Association Methods for Mechanized Documentation: Symposium Proceedings (Vol. 269, p. 61).
    US Government Printing Office.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (a * d - b * c) / math.sqrt((a + b + c + d) * (a + b) * (a + c))


def disperson(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Disperson similarity

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    n = a + b + c + d

    return (a * d - b * c) / (n * n)


def consonni_todeschini5(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Consonni and Todeschini (v5)

    Consonni, V., & Todeschini, R. (2012).
    New similarity coefficients for binary data.
    Match-Communications in Mathematical and Computer Chemistry, 68(2), 581.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    n = a + b + c + d

    return (math.log(1 + a * d) - math.log(1 + b * c)) / math.log(1 + n * n / 4)


def stiles(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Stiles similarity

    Stiles, H. E. (1961).
    The association factor in information retrieval.
    Journal of the ACM (JACM), 8(2), 271-279.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    n = a + b + c + d

    t = abs(a * d - b * c) - 0.5 * n

    return math.log10((n * t * t) / ((a + b) * (a + c) * (b + d) * (c + d)))


def scott(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Scott similarity

    Scott, W. A. (1955).
    Reliability of content analysis: The case of nominal scale coding.
    Public opinion quarterly, 321-325.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (4 * a * d - (b + c) ** 2) / ((2 * a + b + c) * (2 + d + b + c))


def tetrachoric(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Tetrachoric similarity

    Peirce, C. S. (1884).
    The numerical measure of the success of predictions.
    Science, (93), 453-454.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return math.cos(180 / (1 + math.sqrt((a * d) / (b * c))))


def odds_ratio(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Odds ratio

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (a * d) / (b * c)


def rand(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Rand index similarity

    Rand, W. M. (1971).
    Objective criteria for the evaluation of clustering methods.
    Journal of the American Statistical association, 66(336), 846-850.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    n = a + b + c + d

    N = n * (n - 1) / 2
    B = a * b + c * d
    C = a * c + b * d
    D = a * d + b * c
    A = N - B - C - D

    return (A + B) / N


def adjusted_rand(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Adjusted Rand index similarity

    Rand, W. M. (1971).
    Objective criteria for the evaluation of clustering methods.
    Journal of the American Statistical association, 66(336), 846-850.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    n = a + b + c + d

    N = n * (n - 1) / 2
    B = a * b + c * d
    C = a * c + b * d
    D = a * d + b * c
    A = N - B - C - D

    denomi = (A + B) * (A + C) + (C + D) * (B + D)

    return (N * (A + D) - denomi) / (N * N - denomi)


def loevinger_h(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Loevinger's H

    Loevinger, J. (1948).
    The technic of homogeneous tests compared with some aspects of" scale analysis" and factor analysis.
    Psychological bulletin, 45(6), 507.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    p1 = max(a, b) + max(c, d) + max(a, c) + max(b, d)
    p2 = max(a + c, b + d) + max(a + b, c + d)

    return 1 - (b / ((a + b + c + d) * p1 * p2))


def sokal_sneath4(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Sokal-Sneath similarity (v4)

    Sneath, P. H., & Sokal, R. R. (1973).
    Numerical taxonomy.
    The principles and practice of numerical classification.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (a / (a + b) + a / (a + c) + d / (b + d) + d / (c + d)) / 4


def sokal_sneath5(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Sokal-Sneath similarity (v5)

    Sneath, P. H., & Sokal, R. R. (1973).
    Numerical taxonomy.
    The principles and practice of numerical classification.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (a * d) / math.sqrt((a + b) * (a + c) * (b + d) * (c + d))


def rogot_goldberg(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Rogot-Goldberg

    Rogot, E., & Goldberg, I. D. (1966).
    A proposed index for measuring agreement in test-retest studies.
    Journal of chronic diseases, 19(9), 991-1006.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (a / (2 * a + b + c)) + (d / (2 * d + b + c))


def baroni_urbani_buser1(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Baroni-Urbani similarity (v1)

    Baroni-Urbani, C., & Buser, M. W. (1976).
    Similarity of binary data.
    Systematic Zoology, 25(3), 251-259.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (math.sqrt(a * d) + a) / (math.sqrt(a * d) + a + b + c)


def peirce3(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Peirce similarity (v3)

    Peirce, C. S. (1884).
    The numerical measure of the success of predictions.
    Science, (93), 453-454.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (a * b + b * c) / (a * b + 2 * b * c + c * d)


def hawkins_dotson(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Hawkins-Dotson

    Hawkins, R. P., & Dotson, V. A. (1973).
    Reliability Scores That Delude: An Alice in Wonderland Trip Through the Misleading Characteristics of Inter-Observer Agreement Scores in Interval Recording.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return 0.5 * ((a / (a + b + c) + (d / (b + c + d))))


def tarantula(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Tarantula similarity

    Jones, J. A., & Harrold, M. J. (2005, November).
    Empirical evaluation of the tarantula automatic fault-localization technique.
    In Proceedings of the 20th IEEE/ACM international Conference on Automated software engineering (pp. 273-282).

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (a * (c + d)) / (c * (a + b))


def harris_lahey(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Harris-Lahey similarity

    Harris, F. C., & Lahey, B. B. (1978).
    A method for combining occurrence and nonoccurrence interobserver agreement scores.
    Journal of Applied Behavior Analysis, 11(4), 523-527.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return ((a * (2 * d + b + c)) / (2 * (a + b + c))) + (
        (d * (2 * a + b + c) / (2 * (b + c + d)))
    )


def forbes1(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Forbesi similarity (v1)

    Forbes, S. A. (1907).
    On the local distribution of certain Illinois fishes: an essay in statistical ecology (Vol. 7).
    Illinois State Laboratory of Natural History.

    Forbes, S. A. (1925).
    Method of determining and measuring the associative relations of species.
    Science, 61(1585), 518-524.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    n = a + b + c + d

    return (n * a) / ((a + b) * (a + c))


def baroni_urbani_buser2(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Baroni-Urbani similarity (v1)

    Baroni-Urbani, C., & Buser, M. W. (1976).
    Similarity of binary data.
    Systematic Zoology, 25(3), 251-259.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (math.sqrt(a * d) + a - b - c) / (math.sqrt(a * d) + a + b + c)


def fossum(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Fossum similarity

    Holliday, J. D., Hu, C. Y., & Willett, P. (2002).
    Grouping of coefficients for the calculation of inter-molecular similarity and dissimilarity using 2D fragment bit-strings.
    Combinatorial chemistry & high throughput screening, 5(2), 155-166.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    n = a + b + c + d

    return (n * (a - 0.5) ** 2) / math.sqrt((a + b) * (a + c))


def forbes2(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Forbesi similarity (v2)

    Forbes, S. A. (1907).
    On the local distribution of certain Illinois fishes: an essay in statistical ecology (Vol. 7).
    Illinois State Laboratory of Natural History.

    Forbes, S. A. (1925).
    Method of determining and measuring the associative relations of species.
    Science, 61(1585), 518-524.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    n = a + b + c + d

    return (n * a - (a + b) * (a + c)) / (n * min(a + b, a + c) - (a + b) * (a + c))


def eyraud(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Eyraud similarity

    Eyraud, H. (1936).
    Les principes de la mesure des correlations.
    Ann. Univ. Lyon, III. Ser., Sect. A, 1(30-47), 111.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    n = a + b + c + d

    return (n * n * (n * a - (a + b) * (a + c))) / (
        (a + b) * (a + c) * (b + d) * (c + d)
    )


def tarwid(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Tarwid similarity

    Tarwid, K. (1960).
    Szacowanie zbieznosci nisz ekologicznych gatunkow droga oceny prawdopodobienstwa spotykania sie ich w polowach.
    Ecol Polska B (6), 115-130.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    n = a + b + c + d

    return (n * a - (a + b) * (a + c)) / (n * a + (a + b) * (a + c))


def goodman_kruskal1(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Goodman-Kruskal similarity (v1)

    Goodman, L. A., & Kruskal, W. H. (1979).
    Measures of association for cross classifications.
    Measures of association for cross classifications, 2-34.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    n = a + b + c + d

    p1 = max(a, b) + max(c, d) + max(a, c) + max(b, d)
    p2 = max(a + c, b + d) + max(a + b, c + d)

    return (p1 - p2) / (2 * n - p2)


def anderberg(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Anderberg similarity

    Anderberg, M. R. (2014).
    Cluster analysis for applications: probability and mathematical statistics: a series of monographs and textbooks (Vol. 19).
    Academic press.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    n = a + b + c + d

    p1 = max(a, b) + max(c, d) + max(a, c) + max(b, d)
    p2 = max(a + c, b + d) + max(a + b, c + d)

    return (p1 - p2) / (2 * n)


def goodman_kruskal2(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Goodman-Kruskal similarity (v2)

    Goodman, L. A., & Kruskal, W. H. (1979).
    Measures of association for cross classifications.
    Measures of association for cross classifications, 2-34.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    return (2 * min(a, d) - b - c) / (2 * min(a, d) + b + c)


def gilbert_wells(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Gilbert-Wells similarity

    Gilbert, G. K. (1884).
    Finley's tornado predictions. American Meteorological Journal.
    A Monthly Review of Meteorology and Allied Branches of Study (1884-1896), 1(5), 166.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    n = a + b + c + d

    return math.log(a) - math.log(n) - math.log((a + b) / n) - math.log((a + c) / n)


def consonni_todeschini2(
    x: BinaryFeatureVector,
    y: BinaryFeatureVector,
    mask: BinaryFeatureVectorEmpty = None,
) -> float:
    """Consonni and Todeschini (v2)

    Consonni, V., & Todeschini, R. (2012).
    New similarity coefficients for binary data.
    Match-Communications in Mathematical and Computer Chemistry, 68(2), 581.

    Args:
        x (BinaryFeatureVector): binary feature vector
        y (BinaryFeatureVector): binary feature vector

    Returns:
        float: similarity of given vectors
    """
    a, b, c, d = operational_taxonomic_units(x, y, mask)

    n = a + b + c + d

    return (math.log(1 + n) - math.log(1 + b + c)) / math.log(1 + n)
