import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

class SuperHamming {
    public static void main(String[] args) throws IOException {
        String inputFileName = args[0],
                outputFileName = args[1];

        int maxDist = args.length > 2 ? Integer.parseInt(args[2]) : 3;

        System.out.printf("[" + new Date() + "] Started with " + inputFileName);

        final List<String> lines = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader(inputFileName))) {

            String line;

            while ((line = br.readLine()) != null) {
                lines.add(line);
            }
        }

        System.out.printf("[" + new Date() + "] Read file into memory. Comparing.");

        try (PrintWriter output = new PrintWriter(outputFileName)) {
            lines
                    .parallelStream()
                    .flatMap(
                            s1 -> lines
                                    .stream()
                                    .filter(s2 -> s1.compareTo(s2) > 0)
                                    .map(s2 -> new StringTuple(s1, s2))
                    )
                    .filter(t -> t.getOrComputeHamming() <= maxDist)
                    .forEach(output::println);
        }

        System.out.printf("[" + new Date() + "] Done.");
    }

    private static class StringTuple {
        private final String first, second;
        private Integer hamming = null;

        public StringTuple(String first, String second) {
            this.first = first;
            this.second = second;
        }

        public String getFirst() {
            return first;
        }

        public String getSecond() {
            return second;
        }

        private int computeHamming() {
            int dist = 0;

            for (int i = 0; i < first.length(); i++) {
                if (first.charAt(i) != second.charAt(i))
                    dist++;
            }

            return dist;
        }

        public int getOrComputeHamming() {
            if (hamming == null) {
                hamming = computeHamming();
            }

            return hamming;
        }

        @Override
        public String toString() {
            return first + "," + second + "," + hamming;
        }
    }
}
