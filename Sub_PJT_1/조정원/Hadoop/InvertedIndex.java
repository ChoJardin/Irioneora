package ssafy;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.mapreduce.lib.input.FileSplit;

import java.io.IOException;
import java.nio.file.FileSystem;
import java.util.StringTokenizer;

public class InvertedIndex {
	/* 
	Object, Text : input key-value pair type (always same (to get a line of input file))
	Text, IntWritable : output key-value pair type
	*/
	public static class TokenizerMapper
			extends Mapper<Object,Text,Text,Text> {
			// Object, text => key value pair as input
			// Text, IntWritable => key value pair as output 

		// variable declairations
		private final static IntWritable one = new IntWritable(1);
		private Text word = new Text();
		private Text pos = new Text();
		private String filename;
		protcted void setup(Context context) throws IOException, InterruptedException {
			filename = ((FileSplit)context.getInputSplit()).getPath().getName();
		}

		// map function (Context -> fixed parameter)
		public void map(Object key, Text value, Context context)
				throws IOException, InterruptedException {

			// value.toString() : get a line
			StringTokenizer itr = new StringTokenizer(value.toString(), " ", true);
			long p = ((LongWritable)key).get();
			while ( itr.hasMoreTokens() ) {
				String token = itr.nextToken();
				word.set(token.trim());
				if (! token.equals(" ")) {
					pos.set(filename+":"+p);
					context.write(word.pos);
				}
				p += token.length();

			}
		}
	}

	/*
	Text, IntWritable : input key type and the value type of input value list
	Text, IntWritable : output key-value pair type
	*/
	public static class IntSumReducer
			extends Reducer<Text,Text,Text,Text> {

		private Text list - new Text();

		public void reduce(Text key, Iterable<Text> values, Context context)
				throws IOException, InterruptedException {

			String s = new String();
			int comma = 0;
			for (Text val: values) {
				if (comma == 0) {
					comma = 1;
					s += (":"+val.toString());
				}
				else
					s += (",	" + val.toString());
			}
			list.set(s);
			context.write(key,list);

		}
	}


	/* Main function */
	public static void main(String[] args) throws Exception {
		Configuration conf = new Configuration();
		String[] otherArgs = new GenericOptionsParser(conf,args).getRemainingArgs();
		if ( otherArgs.length != 2 ) {
			System.err.println("Usage: <in> <out>");
			System.exit(2);
		}

		// if output file already exists, delete it and run
		FileSystem hdfs = FileSystem.get(conf);
		Path output = new Path(otherArgs[1]);
		if (hdfs.exists(output))
			hdfs.delete(output, true);

		Job job = new Job(conf,"word count");
		job.setJarByClass(InvertedIndex.class);

		// let hadoop know my map and reduce classes
		job.setMapperClass(TokenizerMapper.class);
		job.setReducerClass(IntSumReducer.class);

		job.setOutputKeyClass(Text.class);
		job.setOutputValueClass(Text.class);

		// set number of reduces
		job.setNumReduceTasks(2);

		// set input and output directories
		FileInputFormat.addInputPath(job,new Path(otherArgs[0]));
		FileOutputFormat.setOutputPath(job,new Path(otherArgs[1]));
		System.exit(job.waitForCompletion(true) ? 0 : 1 );
	}
}

