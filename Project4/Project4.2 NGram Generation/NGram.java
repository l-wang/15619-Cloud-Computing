import java.io.IOException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;

public class NGram {

	public static class NGram_M extends Mapper<LongWritable, Text, Text, IntWritable>{
		private static final IntWritable one = new IntWritable(1);
		private Text gram = new Text();
		
		public void map(LongWritable key, Text value, Context context) 
				throws IOException, InterruptedException{
					
			String line = value.toString();
			if (line.length() == 0) return;
			
			line = line.trim().toLowerCase().replaceAll("[^a-zA-Z]+", " ");
			String words[] = line.split(" ");
			
			for (int i = 0; i < words.length ; i++) {
				StringBuilder tmp = new StringBuilder();
				boolean first = true;
				for (int offset = 0; offset < 5 && offset + i < words.length; offset++) {
					if (first) {
						first = false;
					} else {
						tmp.append(" ");
					}
					tmp.append(words[i + offset]);
					gram.set(tmp.toString());
					context.write(gram, one);
				}
			}
		}
	}

	public static class NGram_R extends Reducer<Text, IntWritable, Text, IntWritable>{

		public void reduce(Text key, Iterable<IntWritable> values, Context context) 
				throws IOException, InterruptedException{
			int sum = 0;
			for (IntWritable v : values) {
				sum  += v.get();
			}
			context.write(key, new IntWritable(sum));
		}
	}

	public static void main (String[] args) throws Exception{
		Configuration conf = new Configuration();
		
		Job job = new Job(conf, "NGram_Project4.1");
		job.setJarByClass(NGram.class);

		job.setMapperClass(NGram_M.class);
		job.setCombinerClass(NGram_R.class);
		job.setReducerClass(NGram_R.class);
		
		job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(IntWritable.class);
		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(IntWritable.class);
			
		job.setInputFormatClass(TextInputFormat.class);
		job.setOutputFormatClass(TextOutputFormat.class);
		
		job.setNumReduceTasks(1);
		
		FileInputFormat.addInputPath(job, new Path(args[0]));
		FileOutputFormat.setOutputPath(job, new Path(args[1]));

		System.exit(job.waitForCompletion(true) ? 0 : 1);
	}
}