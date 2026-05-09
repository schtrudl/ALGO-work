import java.io.*;
import java.math.BigDecimal;
import java.util.*;

/**
    Igra nasprotnika 2026 - pokrivanje kosev
    Ekipa: Dejan Jarc, Jure Zupančič

    Uporaba: java bin_cover input_folder_path output_folder_path

    - input_folder_path: pot do mape z vhodnimi datotekami
    - output_folder_path: pot do mape, kamor se bodo shranile izhodne datoteke

    Parametri:
    - largeItemThreshold: velikost, nad katero se šteje, da je predmet velik (npr. 0.5)
    - largeReuseMinLoad: minimalna napolnjenost, pri kateri se lahko velik predmet uporabi za izboljšanje obstoječega kosa (npr. 0.20)
    - largeItemMaxOvershoot: največje dovoljeno preseganje polnosti koša pri dodajanju velikega predmeta (npr. 0.10)
    - largeItemMinBinLoad: prag, pod katerim se koš šteje za šibek, da bi vanj dodali velik predmet (npr. 0.20)
 */

public class bin_cover {

    public static void main(String[] args) throws Exception {
        if (args.length != 2) {
            System.err.println("Usage: java bin_cover <input_folder_path> <output_folder_path>");
            System.exit(1);
        }

        String input = args[0]; // path of input folder
        String output = args[1]; // path of output folder

        // create new solver instance for each input file
        // adjust parameters here if needed
        // initial values set based on testing and benchmarking
        BinCoveringSolver solver = new BinCoveringSolver(
                new BigDecimal("0.71"),     // large item threshold
                new BigDecimal("0.20"),     // reuse minimal load
                new BigDecimal("0.14"),     // large item max overshoot
                new BigDecimal("0.15")      // large item min bin load
        );

        List<BigDecimal> items = readFile(input); // read items from input file
        List<List<Integer>> solution = solver.solve(items); // solve the instance and return solution

        writeSolution(output, solution); // write solution to output file

    }

    // readFile: method for reading item inputs from a file
    private static List<BigDecimal> readFile(String path) throws IOException {
        List<String> tokens = new ArrayList<>();

        try (BufferedReader br = new BufferedReader(new FileReader(path))) {
            String line;
            while ((line = br.readLine()) != null) {
                line = line.trim();
                if (!line.isEmpty()) {
                    tokens.add(line);
                }
            }
        }

        if (tokens.isEmpty()) {
            throw new IllegalArgumentException("Input file is empty.");
        }

        int n = Integer.parseInt(tokens.get(0));
        if (tokens.size() != n + 1) {
            throw new IllegalArgumentException("Expected " + n + " item values, got " + (tokens.size() - 1));
        }

        List<BigDecimal> items = new ArrayList<>();
        for (int i = 1; i <= n; i++) {
            items.add(new BigDecimal(tokens.get(i)));
        }

        return items;
    }

    // writeSolution: write a solution to a file
    private static void writeSolution(String path, List<List<Integer>> coveredBins) throws IOException {
        try (PrintWriter out = new PrintWriter(new FileWriter(path))) {
            out.println(coveredBins.size());
            for (List<Integer> bin : coveredBins) {
                for (int i = 0; i < bin.size(); i++) {
                    if (i > 0) out.print(" ");
                    out.print(bin.get(i));
                }
                out.println();
            }
        }
    }
}

class BinCoveringSolver {
    private static final BigDecimal ONE = BigDecimal.ONE;

    private final BigDecimal largeItemThreshold;
    private final BigDecimal largeReuseMinLoad;
    private final BigDecimal largeItemMaxOvershoot;
    private final BigDecimal largeItemMinBinLoad;

    private final List<Bin> bins = new ArrayList<>();
    private final List<Integer> openBins = new ArrayList<>();
    private final List<Integer> coveredBins = new ArrayList<>();

    // constructor for BinCoveringSolver
    public BinCoveringSolver(BigDecimal largeItemThreshold, BigDecimal largeReuseMinLoad, BigDecimal largeItemMaxOvershoot, BigDecimal largeItemMinBinLoad) {
        this.largeItemThreshold = largeItemThreshold;
        this.largeReuseMinLoad = largeReuseMinLoad;
        this.largeItemMaxOvershoot = largeItemMaxOvershoot;
        this.largeItemMinBinLoad = largeItemMinBinLoad;
    }

    // solve: method for covering bins with the given items
    public List<List<Integer>> solve(List<BigDecimal> items) {
        // Initialize state for a new instance
        bins.clear();
        openBins.clear();
        coveredBins.clear();

        for (int i = 0; i < items.size(); i++) {
            int itemIndex = i + 1; // 1-based indexing for output
            BigDecimal itemSize = items.get(i);
            placeItem(itemIndex, itemSize);
        }

        List<List<Integer>> result = new ArrayList<>();
        for (int binId : coveredBins) {
            result.add(new ArrayList<>(bins.get(binId).itemIndices));
        }
        return result;
    }

    // placeItem: method for placing an item (by index and size) into a bin
    private void placeItem(int itemIndex, BigDecimal itemSize) {
        Integer chosenBinId = chooseBin(itemIndex, itemSize);

        if (chosenBinId == null) {
            chosenBinId = openNewBin();
        }

        Bin bin = bins.get(chosenBinId);
        bin.itemIndices.add(itemIndex);
        bin.total = bin.total.add(itemSize);

        if (!bin.covered && bin.total.compareTo(ONE) >= 0) {
            bin.covered = true;
            coveredBins.add(chosenBinId);
            openBins.remove(Integer.valueOf(chosenBinId));
        }
    }

    // chooseBin: method for selecting the best bin for an item
    private Integer chooseBin(int itemIndex, BigDecimal itemSize) {
        Integer bestCoverBin = null;
        BigDecimal bestCoverLoad = null;

        Integer bestFillBin = null;
        BigDecimal bestFillLoad = null;

        for (int binId : openBins) {
            Bin bin = bins.get(binId);

            if (!canPlace(bin, itemSize, itemIndex)) {
                continue;
            }

            BigDecimal newTotal = bin.total.add(itemSize);

            if (newTotal.compareTo(ONE) >= 0) {
                // Best cover: choose the fullest bin that becomes covered
                if (bestCoverBin == null || bin.total.compareTo(bestCoverLoad) > 0) {
                    bestCoverBin = binId;
                    bestCoverLoad = bin.total;
                }
            } else {
                // Best unfinished fill: choose the fullest unfinished bin
                if (bestFillBin == null || bin.total.compareTo(bestFillLoad) > 0) {
                    bestFillBin = binId;
                    bestFillLoad = bin.total;
                }
            }
        }

        if (bestCoverBin != null) {
            return bestCoverBin;
        }

        // Large item protection:
        // use a large item to strengthen an existing bin only if that bin already looks promising
        if (itemSize.compareTo(largeItemThreshold) >= 0) {
            if (bestFillBin != null && bestFillLoad.compareTo(largeReuseMinLoad) >= 0) {
                return bestFillBin;
            }
            return null;
        }

        if (bestFillBin != null) {
            return bestFillBin;
        }

        return null;
    }

    // canPlace: method for checking if an item can be placed in a bin
    protected boolean canPlace(Bin bin, BigDecimal itemSize, int itemIndex) {
        BigDecimal newTotal = bin.total.add(itemSize);

        // Overshoot test
        if (newTotal.compareTo(ONE) >= 0) {
            BigDecimal overshoot = newTotal.subtract(ONE);
            
            // reject placement if item is too large and overshoot is too big
            if (itemSize.compareTo(largeItemThreshold) >= 0 &&
                overshoot.compareTo(largeItemMaxOvershoot) > 0) {
                return false;
            }
        }

        // Large item protection
        // reject placement of a large item into a weakly covered bin
        if (itemSize.compareTo(largeItemThreshold) >= 0 &&
            bin.total.compareTo(largeItemMinBinLoad) < 0) {
            return false;
        }

        return true;
    }

    // openNewBin: method for opening a new bin
    private int openNewBin() {
        int id = bins.size();
        bins.add(new Bin());
        openBins.add(id);
        return id;
    }
}
// Class for representing a bin (item indices, total fullness and a flag if it's covered)
class Bin {
    List<Integer> itemIndices = new ArrayList<>();
    BigDecimal total = BigDecimal.ZERO;
    boolean covered = false;
}